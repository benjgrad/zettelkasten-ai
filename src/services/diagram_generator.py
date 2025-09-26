import re
import sqlite3
from typing import List, Dict, Any, Set, Tuple
from src.models import db
from src.services.entity_extraction import entity_service

class DiagramGenerator:
    def __init__(self):
        self.entity_colors = {
            "PERSON": "#FFE4B5",  # Moccasin
            "ORG": "#B0E0E6",     # Powder Blue
            "GPE": "#98FB98"      # Pale Green
        }

    def sanitize_id(self, text: str) -> str:
        """Convert text to valid MermaidJS node ID"""
        # Replace spaces and special characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', text)
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = f"N_{sanitized}"
        return sanitized or "node"

    def create_node_definition(self, entity: Dict[str, Any]) -> Tuple[str, str]:
        """Create MermaidJS node definition and styling"""
        node_id = self.sanitize_id(entity["text"])
        label = entity["text"].replace('"', '\\"')  # Escape quotes
        entity_type = entity["label"]

        # Create node with appropriate shape based on type
        if entity_type == "PERSON":
            node_def = f'{node_id}["{label}"]'
        elif entity_type == "ORG":
            node_def = f'{node_id}["{label}"]'
        elif entity_type == "GPE":
            node_def = f'{node_id}["{label}"]'
        else:
            node_def = f'{node_id}["{label}"]'

        # Create styling
        color = self.entity_colors.get(entity_type, "#E0E0E0")
        style_def = f"style {node_id} fill:{color}"

        return node_def, style_def

    def generate_relationships(self, entities: List[Dict[str, Any]]) -> List[str]:
        """Generate relationships between entities"""
        relationships = []

        # Group entities by type
        persons = [e for e in entities if e["label"] == "PERSON"]
        orgs = [e for e in entities if e["label"] == "ORG"]
        gpes = [e for e in entities if e["label"] == "GPE"]

        # Create relationships: PERSON --> ORG
        for person in persons:
            for org in orgs:
                person_id = self.sanitize_id(person["text"])
                org_id = self.sanitize_id(org["text"])
                relationships.append(f"{person_id} --> {org_id}")

        # Create relationships: ORG --> GPE
        for org in orgs:
            for gpe in gpes:
                org_id = self.sanitize_id(org["text"])
                gpe_id = self.sanitize_id(gpe["text"])
                relationships.append(f"{org_id} --> {gpe_id}")

        # If no ORGs, connect PERSON directly to GPE
        if not orgs:
            for person in persons:
                for gpe in gpes:
                    person_id = self.sanitize_id(person["text"])
                    gpe_id = self.sanitize_id(gpe["text"])
                    relationships.append(f"{person_id} --> {gpe_id}")

        # If only one type of entity, create a simple flow
        if len(entities) > 1 and not relationships:
            for i in range(len(entities) - 1):
                current_id = self.sanitize_id(entities[i]["text"])
                next_id = self.sanitize_id(entities[i + 1]["text"])
                relationships.append(f"{current_id} --> {next_id}")

        return relationships

    def generate_mermaid_flowchart(self, entities: List[Dict[str, Any]], title: str = None) -> str:
        """Generate MermaidJS flowchart from entities"""
        if not entities:
            return """flowchart TD
    A["No entities found"]
    style A fill:#FFE4E1"""

        mermaid_lines = ["flowchart TD"]

        # Add title if provided
        if title:
            # Sanitize title for MermaidJS
            clean_title = title.replace('"', '\\"')[:50] + ("..." if len(title) > 50 else "")
            mermaid_lines.append(f'    subgraph Title["{clean_title}"]')
            mermaid_lines.append("    end")

        # Generate nodes
        node_definitions = []
        style_definitions = []
        seen_ids = set()

        for entity in entities:
            node_def, style_def = self.create_node_definition(entity)
            node_id = self.sanitize_id(entity["text"])

            if node_id not in seen_ids:
                node_definitions.append(f"    {node_def}")
                style_definitions.append(f"    {style_def}")
                seen_ids.add(node_id)

        # Generate relationships
        relationships = self.generate_relationships(entities)

        # Add nodes to diagram
        mermaid_lines.extend(node_definitions)

        # Add relationships
        for rel in relationships:
            mermaid_lines.append(f"    {rel}")

        # Add styles
        mermaid_lines.extend(style_definitions)

        return "\n".join(mermaid_lines)

    def generate_diagram_from_article(self, article_id: int) -> Dict[str, Any]:
        """Generate MermaidJS diagram from article entities"""
        try:
            # Get article entities
            entities_result = entity_service.get_article_entities(article_id)

            if "error" in entities_result:
                return {"error": entities_result["error"]}

            entities = entities_result.get("entities", [])

            # Get article title
            with db.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT title FROM articles WHERE id = ?",
                    (article_id,)
                )
                article = cursor.fetchone()

            if not article:
                return {"error": f"Article {article_id} not found"}

            # Generate MermaidJS
            mermaid_code = self.generate_mermaid_flowchart(
                entities,
                title=article["title"]
            )

            return {
                "article_id": article_id,
                "article_title": article["title"],
                "entities_count": len(entities),
                "entities": entities,
                "mermaid_code": mermaid_code,
                "render_url": f"https://mermaid.live/edit#{self._encode_for_url(mermaid_code)}"
            }

        except Exception as e:
            return {"error": f"Diagram generation failed: {str(e)}"}

    def _encode_for_url(self, mermaid_code: str) -> str:
        """Encode MermaidJS code for mermaid.live URL"""
        import base64
        # Encode to base64 for URL
        encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
        return encoded

    def validate_mermaid_syntax(self, mermaid_code: str) -> Dict[str, Any]:
        """Basic validation of MermaidJS syntax"""
        errors = []
        warnings = []

        lines = mermaid_code.split('\n')

        # Check if it starts with flowchart declaration
        if not any(line.strip().startswith('flowchart') for line in lines):
            errors.append("Missing 'flowchart' declaration")

        # Check for basic syntax issues
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('flowchart') or line.startswith('subgraph') or line.startswith('end') or line.startswith('style'):
                continue

            # Check for node definitions and relationships
            if '-->' not in line and '[' not in line and ']' not in line:
                warnings.append(f"Line {i}: Potentially invalid syntax - {line}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "lines_checked": len(lines)
        }

diagram_generator = DiagramGenerator()