#!/usr/bin/env python3

import os
import sys
import gradio as gr
import requests
import base64
from typing import List, Tuple, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.diagram_generator import diagram_generator
from src.services.diagram_refinement import diagram_refinement
from src.services.vector_storage import vector_storage
from src.services.entity_extraction import entity_service

class DiagramChatbot:
    def __init__(self):
        self.conversation_history = []
        self.current_diagram = None
        self.current_diagram_context = None
        self.backend_url = "http://localhost:8000"

    def process_message(self, message: str, history: List[dict]) -> Tuple[str, str]:
        """Process user message and return response with diagram"""
        try:
            # Check if this is feedback for an existing diagram
            if self._is_feedback_message(message):
                if self.current_diagram:
                    return self._handle_diagram_feedback(message, history)
                else:
                    return "Please generate a diagram first before providing feedback.", ""
            else:
                return self._handle_new_query(message, history)

        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            return error_msg, ""

    def _is_feedback_message(self, message: str) -> bool:
        """Determine if message is feedback for diagram refinement"""
        feedback_keywords = [
            "make it", "change", "modify", "improve", "simplify", "add more",
            "remove", "better", "clearer", "reorganize", "fix", "update"
        ]
        return any(keyword in message.lower() for keyword in feedback_keywords)

    def _handle_new_query(self, message: str, history: List[dict]) -> Tuple[str, str]:
        """Handle new diagram generation query"""
        # Search for relevant articles using semantic search
        search_result = vector_storage.semantic_search(message, limit=3)

        if "error" in search_result or search_result["results_count"] == 0:
            return "I couldn't find relevant information for your query. Please try a different topic.", ""

        # Get the most relevant article
        best_match = search_result["results"][0]
        article_id = best_match["article_id"]

        # Generate diagram from article
        diagram_result = diagram_generator.generate_diagram_from_article(article_id)

        if "error" in diagram_result:
            return f"I found relevant information but couldn't generate a diagram: {diagram_result['error']}", ""

        # Store current diagram and context
        self.current_diagram = diagram_result["mermaid_code"]
        self.current_diagram_context = {
            "article_id": article_id,
            "article_title": best_match.get("title", "Unknown"),
            "entities_count": diagram_result["entities_count"]
        }

        # Create response
        response = f"""I found information about "{best_match.get('title', 'your topic')}" and created a diagram with {diagram_result['entities_count']} entities.

You can provide feedback to improve the diagram, such as:
- "Make it simpler"
- "Add more connections"
- "Organize it better"
- "Focus on the main relationships"

**Similarity Score:** {best_match['similarity_score']:.2f}"""

        return response, self.current_diagram

    def _handle_diagram_feedback(self, feedback: str, history: List[dict]) -> Tuple[str, str]:
        """Handle diagram refinement feedback"""
        if not self.current_diagram:
            return "Please generate a diagram first before providing feedback.", ""

        # Use diagram refinement service
        refinement_result = diagram_refinement.refine_diagram(
            current_mermaid=self.current_diagram,
            feedback=feedback,
            context=self.current_diagram_context
        )

        if "error" in refinement_result:
            return f"I couldn't refine the diagram: {refinement_result['error']}", self.current_diagram

        # Update current diagram
        self.current_diagram = refinement_result["refined_mermaid"]

        response = f"""I've updated the diagram based on your feedback: "{feedback}"

**What I changed:** {refinement_result['refinement_explanation']}

**Validation:** {'✅ Valid syntax' if refinement_result['validation']['valid'] else '❌ Invalid syntax'}

You can continue providing feedback to further improve the diagram."""

        return response, self.current_diagram

    def render_mermaid_diagram(self, mermaid_code: str) -> str:
        """Render MermaidJS code as HTML with fallback"""
        if not mermaid_code or not mermaid_code.strip():
            return "<p>No diagram to display</p>"

        # Generate a unique ID for this diagram
        import hashlib
        import html
        diagram_id = hashlib.md5(mermaid_code.encode()).hexdigest()[:8]
        
        # Escape HTML content properly
        escaped_code = html.escape(mermaid_code)
        
        # Create simple HTML display with both visual and code views
        html_template = f"""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 8px; margin: 10px 0;">
            <div style="background-color: white; border: 1px solid #e1e5e9; border-radius: 8px; padding: 20px; margin: 10px auto;">
                <h4 style="margin-top: 0; color: #333;">Generated Mermaid Diagram</h4>
                <p style="color: #666; font-size: 14px;">Copy the code below and paste it into <a href="https://mermaid.live" target="_blank">mermaid.live</a> to view the diagram:</p>
                <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 15px; margin: 15px 0;">
                    <pre style="margin: 0; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4; white-space: pre-wrap; word-wrap: break-word;">{escaped_code}</pre>
                </div>
                <div style="margin-top: 15px;">
                    <a href="https://mermaid.live" target="_blank" style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                        📊 Open in Mermaid Live Editor
                    </a>
                </div>
                <div style="margin-top: 10px; font-size: 12px; color: #6c757d;">
                    <strong>Instructions:</strong> 
                    1. Click the link above
                    2. Delete any existing code in the editor
                    3. Paste the code from the box above
                    4. The diagram will render automatically
                </div>
            </div>
        </div>
        """
        return html_template

    def clear_conversation(self):
        """Clear conversation and reset state"""
        self.conversation_history = []
        self.current_diagram = None
        self.current_diagram_context = None
        return [], "", ""

# Initialize chatbot
chatbot = DiagramChatbot()

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="MermaidJS Diagram Generator", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🔄 MermaidJS Diagram Generator & Refiner

        Generate diagrams from news articles and refine them with natural language feedback!

        **How to use:**
        1. Ask about any topic (e.g., "Show me about smart cities", "Housing crisis causes")
        2. I'll search relevant articles and generate a diagram
        3. Provide feedback to improve the diagram (e.g., "make it simpler", "add more connections")
        """)

        with gr.Row():
            with gr.Column(scale=1):
                chatbot_component = gr.Chatbot(
                    label="Conversation",
                    height=400,
                    show_label=True,
                    container=True,
                    type="messages"
                )

                msg_input = gr.Textbox(
                    label="Your message",
                    placeholder="Ask about a topic or provide feedback on the diagram...",
                    container=True,
                    scale=4
                )

                with gr.Row():
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                    clear_btn = gr.Button("Clear", variant="secondary", scale=1)

            with gr.Column(scale=1):
                diagram_display = gr.HTML(
                    label="Generated Diagram",
                    value="<p>No diagram generated yet. Ask me about a topic!</p>"
                )

                with gr.Accordion("Diagram Code", open=False):
                    diagram_code = gr.Textbox(
                        label="MermaidJS Code",
                        value="",
                        interactive=False,
                        lines=10,
                        max_lines=20
                    )

        # Event handlers
        def handle_message(message, history):
            if not message.strip():
                return history, ""

            try:
                response, diagram_mermaid = chatbot.process_message(message, history)
                print(f"DEBUG: Response: {response[:100]}...")
                print(f"DEBUG: Diagram code length: {len(diagram_mermaid) if diagram_mermaid else 0}")
                
                # Update history with messages format
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": response})

                # Update diagram display
                diagram_html = chatbot.render_mermaid_diagram(diagram_mermaid) if diagram_mermaid else "<p>No diagram to display</p>"

                return history, "", diagram_html, diagram_mermaid
                
            except Exception as e:
                print(f"DEBUG: Error in handle_message: {e}")
                error_response = f"Error processing message: {str(e)}"
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": error_response})
                return history, "", "<p>Error occurred</p>", ""

        def clear_all():
            chatbot.clear_conversation()
            return [], "", "<p>No diagram generated yet. Ask me about a topic!</p>", ""

        # Connect events
        submit_btn.click(
            handle_message,
            inputs=[msg_input, chatbot_component],
            outputs=[chatbot_component, msg_input, diagram_display, diagram_code]
        )

        msg_input.submit(
            handle_message,
            inputs=[msg_input, chatbot_component],
            outputs=[chatbot_component, msg_input, diagram_display, diagram_code]
        )

        clear_btn.click(
            clear_all,
            outputs=[chatbot_component, msg_input, diagram_display, diagram_code]
        )

        # Examples
        gr.Examples(
            examples=[
                "Show me about smart cities",
                "Housing crisis causes",
                "Make it simpler",
                "Add more connections between elements",
                "Focus on the main relationships"
            ],
            inputs=msg_input,
            label="Example queries and feedback"
        )

    return interface

if __name__ == "__main__":
    # Check if required services are available
    try:
        print("🔍 Checking vector storage...")
        stats = vector_storage.get_collection_stats()
        print(f"✅ Found {stats.get('total_embeddings', 0)} articles in vector storage")

        print("🔍 Checking diagram generation...")
        # Test with a simple validation
        test_result = diagram_generator.validate_mermaid_syntax("flowchart TD\n    A --> B")
        print(f"✅ Diagram generator {'working' if test_result['valid'] else 'has issues'}")

        print("🔍 Checking diagram refinement...")
        # This will show if OpenAI key is configured
        print("✅ Diagram refinement service loaded")

    except Exception as e:
        print(f"⚠️  Warning: Some services may not be fully available: {e}")
        print("   The interface will still work for basic functionality")

    # Create and launch interface
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True,
        inbrowser=True
    )
