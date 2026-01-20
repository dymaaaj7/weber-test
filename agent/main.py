"""
AI Web Builder Agent - Main Application
This agent generates complete HTML websites with embedded CSS and JavaScript
based on user requests using OpenAI's GPT API.
"""

import os
import re
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    """Represents a message in the conversation"""

    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime


class AIWebAgent:
    """
    AI-powered web development agent that generates HTML/CSS/JS websites
    based on natural language descriptions.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Web Agent.

        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.conversation_history: List[Message] = []
        self.generated_code: str = ""

        # System prompt that defines the agent's behavior
        self.system_prompt = """You are an expert web developer specializing in modern, clean HTML, CSS, and vanilla JavaScript. Your task is to create complete, professional websites based on user requests.

Rules:
1. Generate a single HTML file with embedded CSS (in <style>) and JavaScript (in <script>)
2. Use modern HTML5 semantic elements, CSS Grid/Flexbox, CSS custom properties
3. Include responsive design for mobile, tablet, and desktop
4. Use modern CSS features (oklch colors, :has(), container queries where appropriate)
5. Ensure accessibility (ARIA labels, semantic HTML, keyboard navigation)
6. Keep JavaScript minimal and focused on necessary interactivity
7. No external libraries or frameworks - pure vanilla HTML/CSS/JS
8. Provide complete, working code that renders immediately
9. Include a proper DOCTYPE, viewport meta tag, and character encoding
10. Use placeholder images from https://via.placeholder.com when images are needed

When the user asks to modify an existing website, update the entire HTML file with the changes applied.

Respond with the complete HTML code within \`\`\`html and \`\`\` code blocks. Add a brief explanation before the code block."""

    def set_api_key(self, api_key: str) -> None:
        """Set or update the OpenAI API key"""
        self.api_key = api_key

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history

        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        message = Message(role=role, content=content, timestamp=datetime.now())
        self.conversation_history.append(message)

    def extract_code_from_response(self, response: str) -> tuple[str, str]:
        """
        Extract HTML code and explanation from the AI response.

        Args:
            response: Full response from AI

        Returns:
            Tuple of (explanation, code) where explanation is text before code blocks
            and code is the extracted HTML
        """
        # Try to extract code from ```html``` blocks
        code_block_match = re.search(r"```html\n([\s\S]*?)\n```", response)

        if code_block_match:
            code = code_block_match.group(1).strip()
            # Get explanation as everything before the code block
            explanation = response[: code_block_match.start()].strip()
            return explanation, code

        # Try without language specifier
        generic_block_match = re.search(r"```\n([\s\S]*?)\n```", response)

        if generic_block_match:
            code = generic_block_match.group(1).strip()
            # Get explanation as everything before the code block
            explanation = response[: generic_block_match.start()].strip()
            return explanation, code

        # If no code block found, return entire response as explanation
        return response, ""

    async def generate_website(self, user_request: str) -> Dict[str, str]:
        """
        Generate a website based on user request.

        Args:
            user_request: Natural language description of the website

        Returns:
            Dictionary containing:
                - 'code': The generated HTML code
                - 'explanation': The AI's explanation
                - 'error': Error message if any
        """
        if not self.api_key:
            return {
                "code": "",
                "explanation": "",
                "error": "API key not set. Please set your OpenAI API key.",
            }

        # Add user message to history
        self.add_message("user", user_request)

        try:
            # Prepare messages for API call
            messages = [
                {"role": "system", "content": self.system_prompt},
                *[
                    {"role": msg.role, "content": msg.content}
                    for msg in self.conversation_history[
                        -10:
                    ]  # Keep last 10 messages for context
                ],
            ]

            # Call OpenAI API (placeholder - actual implementation will use async HTTP client)
            # This is a simplified version - in production, use httpx or aiohttp
            response_text = await self._call_openai_api(messages)

            # Extract code and explanation from response
            explanation, generated_code = self.extract_code_from_response(response_text)

            # Store the generated code
            self.generated_code = generated_code

            # Add assistant response to history
            self.add_message("assistant", response_text)

            return {"code": generated_code, "explanation": explanation, "error": ""}

        except Exception as e:
            error_msg = f"Error generating website: {str(e)}"
            print(error_msg)
            return {"code": "", "explanation": "", "error": error_msg}

    async def _call_openai_api(self, messages: List[Dict[str, str]]) -> str:
        """
        Call OpenAI API to generate website code.

        Args:
            messages: List of message dictionaries

        Returns:
            AI response text
        """
        import httpx

        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.7,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history as a list of dictionaries.

        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in self.conversation_history
        ]

    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []
        self.generated_code = ""

    def save_code_to_file(self, filepath: str) -> None:
        """
        Save the generated code to a file.

        Args:
            filepath: Path where to save the HTML file
        """
        if self.generated_code:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.generated_code)


# Example usage
async def main():
    """Example of how to use the AI Web Agent"""
    # Initialize agent with API key
    agent = AIWebAgent(api_key="your-api-key-here")

    # Generate a website
    result = await agent.generate_website(
        "Create a landing page for a coffee shop with a hero section, menu, and contact form"
    )

    if result["error"]:
        print(f"Error: {result['error']}")
    else:
        print("Website generated successfully!")
        print(f"Code length: {len(result['code'])} characters")

        # Save to file
        agent.save_code_to_file("output/website.html")
        print("Saved to output/website.html")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
