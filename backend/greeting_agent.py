# greeting_agent.py
import os
import asyncio
import google.generativeai as genai
from a2a.server import A2AServer, IncomingRequest
from a2a.message import Message, TextPart

# The client is configured via GOOGLE_API_KEY in the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class GreetingAgent(A2AServer):
    def __init__(self):
        super().__init__()
        # Using a powerful text model
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print("[GreetingAgent] Gemini text model initialized.")

    async def handle_message(self, request: IncomingRequest) -> Message:
        prompt_text = request.message.get_text()
        print(f"[GreetingAgent] Received text prompt: '{prompt_text}'")
        
        try:
            response = await self.model.generate_content_async(prompt_text)
            greeting_text = response.text
        except Exception as e:
            greeting_text = f"Error generating text: {e}"

        print("[GreetingAgent] Responding with generated text.")
        return Message(parts=[TextPart(text=greeting_text)])