# greeting_agent.py
import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from python_a2a import A2AServer, Message, TextContent, MessageRole

load_dotenv()

class GreetingAgent(A2AServer):
    def __init__(self):
        super().__init__()
        # Using a powerful text model
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        print("[GreetingAgent] Gemini text model initialized.")

    async def handle_message(self, message: Message) -> Message:
        prompt_text = message.content.text
        print(f"[GreetingAgent] Received text prompt: '{prompt_text}'")
        
        try:
            response = await self.client.agenerate_content(
                model='gemini-1.5-pro-latest',
                contents=prompt_text
            )
            greeting_text = response.text
        except Exception as e:
            greeting_text = f"Error generating text: {e}"

        print("[GreetingAgent] Responding with generated text.")
        return Message(content=TextContent(text=greeting_text), role=MessageRole.AGENT)