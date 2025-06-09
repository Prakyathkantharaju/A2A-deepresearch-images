# image_agent.py
import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from python_a2a import A2AServer, Message, TextContent, MessageRole
from PIL import Image
import io

load_dotenv()

class ImageAgent(A2AServer):
    def __init__(self):
        super().__init__()
        # The latest Pro model can generate images
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        print("[ImageAgent] Gemini image model initialized.")

    async def handle_message(self, message: Message) -> Message:
        prompt = message.content.text
        print(f"[ImageAgent] Received image prompt: '{prompt}'")
        
        try:
            # Generate the image content
            response = await self.client.agenerate_content(
                model='gemini-1.5-pro-latest',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="image/png"
                )
            )
            
            # The response part is an image; save it to a file
            image_data = response.parts[0].blob.data
            image = Image.open(io.BytesIO(image_data))
            output_path = "generated_image.png"
            image.save(output_path)
            response_text = f"Image generated successfully and saved to '{output_path}'"
            
        except Exception as e:
            response_text = f"Error generating image: {e}"
        
        print(f"[ImageAgent] Responding with status: '{response_text}'")
        return Message(content=TextContent(text=response_text), role=MessageRole.AGENT)