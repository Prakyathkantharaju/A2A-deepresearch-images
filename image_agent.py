# image_agent.py
import os
import asyncio
import google.generativeai as genai
from a2a.server import A2AServer, IncomingRequest
from a2a.message import Message, TextPart
from PIL import Image
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ImageAgent(A2AServer):
    def __init__(self):
        super().__init__()
        # The latest Pro model can generate images
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print("[ImageAgent] Gemini image model initialized.")

    async def handle_message(self, request: IncomingRequest) -> Message:
        prompt = request.message.get_text()
        print(f"[ImageAgent] Received image prompt: '{prompt}'")
        
        try:
            # Generate the image content
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
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
        return Message(parts=[TextPart(text=response_text)])