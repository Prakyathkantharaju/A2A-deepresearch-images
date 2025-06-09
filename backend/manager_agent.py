# manager_agent.py
import os
import asyncio
import google.generativeai as genai
from a2a.server import A2AServer, IncomingRequest
from a2a.client import A2AClient
from a2a.message import Message, TextPart

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

ROUTING_PROMPT_TEMPLATE = """
You are an intelligent routing agent. Your job is to analyze a user's request and choose the correct specialist agent to handle it. You must respond with only the agent's name.

The available specialist agents are:
1. 'greeting_agent': Select this for requests involving writing text, creating messages, drafting emails, or answering questions.
2. 'image_agent': Select this for requests to create, draw, generate, or make an image, picture, or visual.

User Request: "{query}"
Chosen Agent:
"""

class ManagerAgent(A2AServer):
    def __init__(self):
        super().__init__()
        self.routing_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        self.specialists = {
            "greeting_agent": A2AClient.from_card_file("./greeting_agent_card.json"),
            "image_agent": A2AClient.from_card_file("./image_agent_card.json")
        }
        print("[ManagerAgent] Router initialized.")

    async def handle_message(self, request: IncomingRequest) -> Message:
        user_query = request.message.get_text()
        print(f"\n[ManagerAgent] Received query: '{user_query}'")
        
        try:
            # 1. Use Gemini to make a routing decision
            prompt = ROUTING_PROMPT_TEMPLATE.format(query=user_query)
            response = await self.routing_model.generate_content_async(prompt)
            chosen_agent_name = response.text.strip().lower().replace("'", "").replace('"', '')
            
            print(f"[ManagerAgent] Routing decision: Call '{chosen_agent_name}'")

            # 2. Delegate the task to the chosen specialist
            if chosen_agent_name in self.specialists:
                specialist_client = self.specialists[chosen_agent_name]
                message_to_specialist = Message(parts=[TextPart(text=user_query)])
                
                final_response = await specialist_client.send_message(message_to_specialist)
                response_text = final_response.get_text()
            else:
                response_text = f"Routing error: Could not find a specialist named '{chosen_agent_name}'."
        
        except Exception as e:
            response_text = f"An error occurred in the ManagerAgent: {e}"

        return Message(parts=[TextPart(text=response_text)])