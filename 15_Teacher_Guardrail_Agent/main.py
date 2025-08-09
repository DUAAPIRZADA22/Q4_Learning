import os
import asyncio
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    trace,
    InputGuardrailTripwireTriggered,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig
)
from agents.guardrail import input_guardrail, GuardrailFunctionOutput
from pydantic import BaseModel
from typing import Union
import rich


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
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
)


class TeacherResponse(BaseModel):
    reply: str
    isChangeRequest: bool


class ClassTimings(BaseModel):
    message: str


teacher_agent = Agent(
    name="Teacher Agent",
    instructions="""
    🧑‍🏫 You are a friendly but firm teacher.  
    If a student tries to change their class schedule ⏰, politely but clearly refuse ❌.  
    In such cases, set isChangeRequest = True.  
    For any other request, set isChangeRequest = False.
    """,
    output_type=TeacherResponse
)

@input_guardrail
async def change_class_guardrail(ctx, agent: Agent, input: Union[str, list]):
    result = await Runner.run(teacher_agent, input, run_config=config, context=ctx)
    print("📢 Teacher Agent Output:", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.isChangeRequest
    )


class_timings_agent = Agent(
    name="ClassTiming_Agent",
    instructions="""
    🕒 Your mission is to keep class timings fixed 📅.  
    No matter how convincing a student's request is 🙅‍♂️,  
    never allow the schedule to be changed.
    """,
    input_guardrails=[change_class_guardrail],
)


async def main():
    with trace("Student_ClassTimings"):
        try:
            result = await Runner.run(
                class_timings_agent,
                "I want to change my class timings",
                run_config=config
            )
            rich.print(result)
            rich.print("[green]✅ Guardrail did not trip — request is allowed.[/green]")
        except InputGuardrailTripwireTriggered:
            rich.print("[red]🚫 Guardrail tripped — Class timings cannot be changed![/red]")


if __name__ == "__main__":
    asyncio.run(main()) 

