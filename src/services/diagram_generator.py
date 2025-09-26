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
        """Enhanced validation of MermaidJS syntax with detailed error detection"""
        errors = []
        warnings = []

        lines = mermaid_code.split('\n')

        # Check if it starts with flowchart declaration
        flowchart_found = False
        for line in lines:
            if line.strip().startswith('flowchart'):
                flowchart_found = True
                # Validate flowchart direction
                parts = line.strip().split()
                if len(parts) == 2 and parts[1] not in ['TD', 'TB', 'BT', 'RL', 'LR']:
                    warnings.append(f"Unknown flowchart direction '{parts[1]}'. Valid: TD, TB, BT, RL, LR")
                break

        if not flowchart_found:
            errors.append("Missing 'flowchart' declaration at start")

        # Enhanced syntax validation
        for i, line in enumerate(lines, 1):
            line_orig = line
            line = line.strip()

            # Skip empty lines and known valid constructs
            if not line or line.startswith('flowchart') or line.startswith('subgraph') or line.startswith('end'):
                continue

            # Validate style definitions
            if line.startswith('style'):
                error_msg = self._validate_style_line(line, i)
                if error_msg:
                    errors.append(error_msg)
                continue

            # Validate node definitions and relationships
            if '-->' in line:
                error_msg = self._validate_relationship_line(line, i)
                if error_msg:
                    errors.append(error_msg)
            elif '[' in line and ']' in line and '-->' not in line:
                error_msg = self._validate_node_line(line, i)
                if error_msg:
                    errors.append(error_msg)
            else:
                # Check for common mistakes
                if any(char in line for char in ['(', ')', '{', '}']) and not line.startswith('subgraph'):
                    warnings.append(f"Line {i}: Possible invalid node syntax - use square brackets [] for nodes")
                elif line and not line.startswith(' '):
                    warnings.append(f"Line {i}: Content should be indented in flowchart")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "lines_checked": len(lines)
        }

    def _validate_style_line(self, line: str, line_num: int) -> str:
        """Validate style definition syntax"""
        parts = line.split()
        if len(parts) < 3:
            return f"Line {line_num}: Style definition incomplete - format: 'style nodeId fill:#color'"

        if not parts[1].replace('_', '').replace('-', '').isalnum():
            return f"Line {line_num}: Invalid node ID '{parts[1]}' in style definition"

        style_props = ' '.join(parts[2:])
        if 'fill:' in style_props and not any(c in style_props for c in ['#', 'rgb', 'hsl']):
            return f"Line {line_num}: Invalid color format in style - use #hex, rgb(), or hsl()"

        return None

    def _validate_relationship_line(self, line: str, line_num: int) -> str:
        """Validate relationship/arrow syntax"""
        if '-->' not in line:
            return None

        parts = line.split('-->')
        if len(parts) != 2:
            return f"Line {line_num}: Invalid relationship syntax - use 'nodeA --> nodeB'"

        left_part = parts[0].strip()
        right_part = parts[1].strip()

        # Validate node identifiers
        if not left_part or not right_part:
            return f"Line {line_num}: Missing node identifier in relationship"

        # Extract node IDs (handle both simple IDs and node definitions)
        left_node = self._extract_node_id(left_part)
        right_node = self._extract_node_id(right_part)

        if not left_node or not right_node:
            return f"Line {line_num}: Unable to extract valid node identifiers from relationship"

        # Check for valid node IDs
        for node, side in [(left_node, 'left'), (right_node, 'right')]:
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', node):
                return f"Line {line_num}: Invalid {side} node ID '{node}' - use alphanumeric and underscore only"

        return None

    def _extract_node_id(self, node_part: str) -> str:
        """Extract node ID from either simple ID or node definition"""
        # If it contains brackets, extract the ID before the first bracket
        if '[' in node_part:
            return node_part.split('[')[0].strip()
        # Otherwise, it's just a simple node ID
        return node_part.strip()

    def _validate_node_line(self, line: str, line_num: int) -> str:
        """Validate node definition syntax"""
        # Check for balanced brackets
        if line.count('[') != line.count(']'):
            return f"Line {line_num}: Unbalanced square brackets in node definition"

        # Check for quotes balance in node labels
        quote_count = line.count('"')
        if quote_count % 2 != 0:
            return f"Line {line_num}: Unbalanced quotes in node label"

        # Extract node ID (before the first bracket)
        if '[' in line:
            node_id = line.split('[')[0].strip()
            if node_id:
                if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', node_id):
                    return f"Line {line_num}: Invalid node ID '{node_id}' - must start with letter, use alphanumeric and underscore only"

        # Check for common syntax errors
        if '[' in line and ']' in line:
            bracket_content = line[line.find('[')+1:line.rfind(']')]
            if bracket_content.startswith('"') and bracket_content.endswith('"'):
                # Valid quoted content
                pass
            elif '"' in bracket_content:
                return f"Line {line_num}: Inconsistent quoting in node label - quote entire label or none"

        return None

diagram_generator = DiagramGenerator()