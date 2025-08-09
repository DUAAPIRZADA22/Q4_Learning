import os
import requests
import rich
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY environment variable is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

@function_tool
def current_location() -> str:
    """Returns current location using public IP info."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        city = data.get("city", "Unknown City")
        country = data.get("country", "Unknown Country")
        return f"📌 Your current location is: {city}, {country}."
    except Exception as e:
        return f"❗ Unable to fetch location. Error: {str(e)}"

@function_tool
def breaking_news() -> str:
    """Returns a mock breaking news update."""
    return "🗞️ Latest News: AI agents are reshaping education and software development!"

plant_agent = Agent(
    name="Plant Agent",
    instructions="You are a specialist in plant science. Provide clear answers for topics related to plants, including photosynthesis.",
)

main_agent = Agent(
    name="Main Agent",
    instructions="You are a friendly and knowledgeable assistant. Use the available tools for general queries and forward any plant-related questions to the Plant Agent.",
    tools=[current_location, breaking_news],
    handoffs=[plant_agent]
)

query = """
1. What is my current location?
2. Any breaking news?
3. What is photosynthesis?
"""

result = Runner.run_sync(
    main_agent,
    query,
    run_config=config
)

print("Last Agent Used:", result.last_agent.name if result.last_agent else "Unknown")
for item in result.new_items:
    rich.print(item)
print("=" * 50)
print("Final Output:")
rich.print(result.final_output)

