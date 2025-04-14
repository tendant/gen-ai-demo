from pydantic_ai import Agent
from app.models import TaskOutput

agent = Agent(
    model='openai:gpt-4o',
    result_type=TaskOutput,
    system_prompt='Generate a task title and priority based on the description.'
)

def generate_task(prompt: str) -> TaskOutput:
    return agent.run_sync(prompt).data