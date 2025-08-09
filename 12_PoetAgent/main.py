import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from rich import print
from rich.panel import Panel
from rich.console import Console

# Load API key from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# 1️⃣ Set up Gemini client
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 2️⃣ Set up Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

# 3️⃣ Create RunConfig (correct variable name used here)
config = RunConfig(
    model=model,
    tracing_disabled=True,
)

# 4️⃣ Specialist Agents
lyric_agent = Agent(
    name="Lyric Poetry Analyst",
    instructions="""
You are a Lyric Poetry Analyst.

Your role:
- Focus on poems that express deep personal feelings or emotions.
- Carefully interpret the mood, tone, and hidden thoughts of the poet.
- Provide a short interpretation (8–10 lines) in English summarizing the emotional core.
""",
    model=model,
)

narrative_agent = Agent(
    name="Narrative Poetry Analyst",
    instructions="""
You are a Narrative Poetry Analyst.

Your role:
- Focus on poems that tell a story or describe a sequence of events.
- Identify characters, setting, and what happens in the poem.
- Summarize the story in 8–10 lines, clearly explaining the main plot or message.
""",
    model=model,
)

dramatic_agent = Agent(
    name="🎭 Dramatic Poetry Analyst",
    instructions="""
You are a Dramatic Poetry Analyst.

Your role:
- Focus on poems meant to be performed, especially monologues or dialogues.
- Analyze the speaker’s voice, conflict, and dramatic impact.
- Provide a brief interpretation (8–10 lines) that explains the situation and tone.
""",
    model=model,
)

# 5️⃣ Triage Agent (Main Router)
triage_agent = Agent(
    name="Poetry Triage Agent",
    instructions="""
You are the Poetry Triage Agent.

Step 1: Read the input poem carefully.

Step 2: Identify which category it belongs to:
- Lyric: Expresses personal feelings or emotions.
- Narrative: Tells a story with characters and a plot.
- Dramatic: Intended for performance with monologue or dialogue.

Step 3: Forward the poem to the most appropriate specialist agent.
""",
    handoffs=[
        lyric_agent,
        narrative_agent,
        dramatic_agent,
    ],
    model=model,
)

# 6️⃣ Main Function
async def main():
    poem = """
He walked alone down empty lanes,
Past broken signs and window panes.
A letter clutched tight in his hand,
From lands afar, a distant strand.
He stopped beneath the old street light,
And vanished softly into the night.
"""

    result = await Runner.run(triage_agent, poem, run_config=config)

    console = Console()
    console.print(Panel("[bold yellow]🔍 Analyzing your poem...[/bold yellow]"))

    console.print("\n[bold green]✅ Final Output:[/bold green]")
    console.print(result.final_output.strip())

    console.print("\n[bold red]💡 Last agent used:[/bold red]", result.last_agent.name)

    console.print("\n[bold yellow]🧾 Your Poem:[/bold yellow]")
    console.print(Panel(poem.strip(), border_style="yellow"))

# 7️⃣ Run the app
if __name__ == "__main__":
    asyncio.run(main())
