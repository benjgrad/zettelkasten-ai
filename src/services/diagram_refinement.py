import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from src.services.diagram_generator import diagram_generator

# Load environment variables from .env file
load_dotenv()

class DiagramRefinementService:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the diagram refinement service with OpenAI integration"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.model = "gpt-4o"

    def _get_client(self):
        """Lazy initialization of OpenAI client"""
        if self.client is None:
            if not self.api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            self.client = OpenAI(api_key=self.api_key)
        return self.client

    def refine_diagram(self, current_mermaid: str, feedback: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Refine a MermaidJS diagram based on user feedback

        Args:
            current_mermaid: The current MermaidJS code
            feedback: User feedback for refinement (e.g., "make it simpler")
            context: Optional context about the diagram (entities, article title, etc.)

        Returns:
            Dict with refined diagram, explanation, and validation results
        """
        try:
            # Validate current diagram first
            validation_result = diagram_generator.validate_mermaid_syntax(current_mermaid)
            if not validation_result["valid"]:
                return {
                    "error": f"Current diagram has validation errors: {validation_result['errors']}"
                }

            # Build refinement prompt
            refinement_prompt = self._build_refinement_prompt(current_mermaid, feedback, context)

            # Call OpenAI to refine the diagram
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in MermaidJS diagram creation and refinement. You help users improve their diagrams based on feedback while maintaining valid syntax."
                    },
                    {
                        "role": "user",
                        "content": refinement_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )

            # Parse response and extract refined diagram
            response_content = response.choices[0].message.content
            refined_result = self._parse_refinement_response(response_content)

            if "error" in refined_result:
                return refined_result

            # Validate refined diagram
            refined_validation = diagram_generator.validate_mermaid_syntax(refined_result["refined_mermaid"])

            return {
                "original_mermaid": current_mermaid,
                "refined_mermaid": refined_result["refined_mermaid"],
                "refinement_explanation": refined_result["explanation"],
                "feedback_applied": feedback,
                "validation": refined_validation,
                "render_url": f"https://mermaid.live/edit#{diagram_generator._encode_for_url(refined_result['refined_mermaid'])}",
                "context": context or {}
            }

        except Exception as e:
            return {"error": f"Diagram refinement failed: {str(e)}"}

    def iterative_refinement(self, initial_mermaid: str, feedback_sequence: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Apply multiple rounds of refinement based on a sequence of feedback

        Args:
            initial_mermaid: Starting MermaidJS diagram
            feedback_sequence: List of feedback strings to apply in sequence
            context: Optional context about the diagram

        Returns:
            Dict with refinement history and final result
        """
        refinement_history = []
        current_diagram = initial_mermaid

        for i, feedback in enumerate(feedback_sequence):
            refinement_result = self.refine_diagram(current_diagram, feedback, context)

            if "error" in refinement_result:
                return {
                    "error": f"Refinement failed at iteration {i+1}: {refinement_result['error']}",
                    "refinement_history": refinement_history
                }

            refinement_history.append({
                "iteration": i + 1,
                "feedback": feedback,
                "input_diagram": current_diagram,
                "output_diagram": refinement_result["refined_mermaid"],
                "explanation": refinement_result["refinement_explanation"],
                "validation": refinement_result["validation"]
            })

            current_diagram = refinement_result["refined_mermaid"]

        return {
            "initial_diagram": initial_mermaid,
            "final_diagram": current_diagram,
            "refinement_history": refinement_history,
            "total_iterations": len(feedback_sequence),
            "final_render_url": f"https://mermaid.live/edit#{diagram_generator._encode_for_url(current_diagram)}"
        }

    def _build_refinement_prompt(self, current_mermaid: str, feedback: str, context: Dict[str, Any] = None) -> str:
        """Build the prompt for OpenAI refinement"""
        prompt_parts = [
            "Please refine the following MermaidJS flowchart diagram based on the user feedback.",
            "",
            "Current MermaidJS diagram:",
            "```mermaid",
            current_mermaid,
            "```",
            "",
            f"User feedback: {feedback}",
            ""
        ]

        if context:
            prompt_parts.extend([
                "Additional context:",
                f"- Article title: {context.get('article_title', 'N/A')}",
                f"- Entities: {context.get('entities_count', 0)} entities",
                ""
            ])

        prompt_parts.extend([
            "Instructions:",
            "1. Apply the user feedback to improve the diagram",
            "2. Maintain valid MermaidJS syntax",
            "3. Keep the core information while making the requested changes",
            "4. If feedback is unclear, make reasonable improvements",
            "",
            "Please respond in this exact format:",
            "",
            "EXPLANATION:",
            "[Explain what changes you made and why]",
            "",
            "REFINED_DIAGRAM:",
            "```mermaid",
            "[Put the refined MermaidJS code here]",
            "```"
        ])

        return "\n".join(prompt_parts)

    def _parse_refinement_response(self, response_content: str) -> Dict[str, Any]:
        """Parse OpenAI response to extract explanation and refined diagram"""
        try:
            # Look for EXPLANATION and REFINED_DIAGRAM sections
            lines = response_content.split('\n')

            explanation = ""
            refined_mermaid = ""

            in_explanation = False
            in_diagram = False

            for line in lines:
                line = line.strip()

                if line.startswith("EXPLANATION:"):
                    in_explanation = True
                    in_diagram = False
                    continue
                elif line.startswith("REFINED_DIAGRAM:"):
                    in_explanation = False
                    continue
                elif line.startswith("```mermaid"):
                    in_diagram = True
                    continue
                elif line.startswith("```") and in_diagram:
                    in_diagram = False
                    continue

                if in_explanation and line:
                    explanation += line + " "
                elif in_diagram and line:
                    refined_mermaid += line + "\n"

            if not refined_mermaid.strip():
                return {"error": "Could not extract refined diagram from response"}

            return {
                "explanation": explanation.strip() or "Diagram refined based on feedback",
                "refined_mermaid": refined_mermaid.strip()
            }

        except Exception as e:
            return {"error": f"Failed to parse refinement response: {str(e)}"}

# Create service instance
diagram_refinement = DiagramRefinementService()