# greeting_agent.py
import os
import asyncio
import sys
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
from python_a2a import A2AServer, Message, TextContent, MessageRole

# Add the agents src directory to Python path
agents_src_path = Path(__file__).parent / "agents" / "src"
if str(agents_src_path) not in sys.path:
    sys.path.insert(0, str(agents_src_path))

# Import the research agent graph
try:
    from agent import graph

    RESEARCH_AGENT_AVAILABLE = True
    print("[GreetingAgent] Research agent graph imported successfully.")
except ImportError as e:
    print(f"[GreetingAgent] Could not import research agent: {e}")
    RESEARCH_AGENT_AVAILABLE = False

load_dotenv()


class GreetingAgent(A2AServer):
    def __init__(self):
        super().__init__()
        # Using a powerful text model as fallback
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        print("[GreetingAgent] Gemini model initialized with research capabilities.")

    def is_research_query(self, query: str) -> bool:
        """Determine if the query requires research capabilities."""
        research_keywords = [
            "who",
            "what",
            "when",
            "where",
            "why",
            "how",
            "latest",
            "recent",
            "current",
            "news",
            "update",
            "winner",
            "champion",
            "result",
            "score",
            "data",
            "statistics",
            "facts",
            "information",
            "research",
            "find",
            "search",
            "look up",
            "tell me about",
            "explain",
            "compare",
            "list",
            "top",
            "best",
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in research_keywords)

    async def handle_message(self, message: Message) -> Message:
        user_query = message.content.text
        print(f"[GreetingAgent] Received query: '{user_query}'")

        # Check if this requires research and if research agent is available
        if RESEARCH_AGENT_AVAILABLE and self.is_research_query(user_query):
            print("[GreetingAgent] Using research agent for comprehensive answer...")
            try:
                # Use the research agent graph
                state = graph.invoke(
                    {
                        "messages": [{"role": "user", "content": user_query}],
                        "max_research_loops": 2,
                        "initial_search_query_count": 3,
                    }
                )

                # Extract the final response
                if "messages" in state and len(state["messages"]) > 1:
                    final_response = state["messages"][-1].content
                else:
                    final_response = f"Research completed but no response generated for: {user_query}"

                print("[GreetingAgent] Research completed successfully")
                return Message(
                    content=TextContent(text=final_response), role=MessageRole.AGENT
                )

            except Exception as e:
                print(f"[GreetingAgent] Research agent error: {e}")
                # Fall back to regular Gemini response
                return await self._generate_regular_response(user_query)
        else:
            # Use regular Gemini for simple queries or when research agent unavailable
            print("[GreetingAgent] Using regular Gemini response...")
            return await self._generate_regular_response(user_query)

    async def _generate_regular_response(self, prompt_text: str) -> Message:
        """Generate a regular response using Gemini."""
        try:
            response = await self.client.agenerate_content(
                model="gemini-1.5-pro-latest", contents=prompt_text
            )
            response_text = response.text
        except Exception as e:
            response_text = f"Error generating response: {e}"

        print("[GreetingAgent] Responding with generated text.")
        return Message(content=TextContent(text=response_text), role=MessageRole.AGENT)
