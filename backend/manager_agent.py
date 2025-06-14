# manager_agent.py
import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from python_a2a import A2AServer, A2AClient, Message, TextContent, MessageRole

load_dotenv()

ROUTING_PROMPT_TEMPLATE = """
You are an intelligent routing agent. Your job is to analyze a user's request and choose the correct specialist agent to handle it. You must respond with only the agent's name.

The available specialist agents are:
1. 'greeting_agent': Select this for requests involving:
   - Writing text, creating messages, drafting emails
   - Answering questions that require research or factual information
   - Looking up current information, news, or recent events
   - Providing explanations, comparisons, or analysis
   - Any query asking "who", "what", "when", "where", "why", or "how"
   - Questions about winners, champions, results, statistics, or data
   - Research requests or information gathering tasks

2. 'image_agent': Select this ONLY for requests that explicitly ask to:
   - Create, draw, generate, or make an image, picture, or visual
   - Design something visual like logos, artwork, or illustrations
   - Generate visual content or graphics

IMPORTANT: If the user is asking for information, facts, research, or wants to know something (even if it might be enhanced with visuals), route to 'greeting_agent' which has research capabilities. Only route to 'image_agent' if the PRIMARY request is to create visual content.

User Request: "{query}"
Chosen Agent:
"""


class ManagerAgent(A2AServer):
    def __init__(self):
        super().__init__()
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.specialists = {
            "greeting_agent": A2AClient(endpoint_url="http://127.0.0.1:8001"),
            "image_agent": A2AClient(endpoint_url="http://127.0.0.1:8003"),
        }
        print("[ManagerAgent] Router initialized with research-capable greeting agent.")

    async def handle_message(self, message: Message) -> Message:
        user_query = message.content.text
        print(f"\n[ManagerAgent] Received query: '{user_query}'")

        try:
            # 1. Use Gemini to make a routing decision
            prompt = ROUTING_PROMPT_TEMPLATE.format(query=user_query)
            response = await self.client.agenerate_content(
                model="gemini-1.5-flash-latest", contents=prompt
            )
            chosen_agent_name = (
                response.text.strip().lower().replace("'", "").replace('"', "")
            )

            print(f"[ManagerAgent] Routing decision: Call '{chosen_agent_name}'")

            # 2. Delegate the task to the chosen specialist
            if chosen_agent_name in self.specialists:
                specialist_client = self.specialists[chosen_agent_name]
                message_to_specialist = Message(
                    content=TextContent(text=user_query), role=MessageRole.USER
                )

                final_response = await specialist_client.send_message(
                    message_to_specialist
                )
                response_text = final_response.content.text
            else:
                response_text = f"Routing error: Could not find a specialist named '{chosen_agent_name}'. Available agents: {', '.join(self.specialists.keys())}"

        except Exception as e:
            response_text = f"An error occurred in the ManagerAgent: {e}"

        return Message(content=TextContent(text=response_text), role=MessageRole.AGENT)
