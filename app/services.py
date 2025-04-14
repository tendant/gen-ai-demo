from pydantic_ai.openai import OpenAIPredictor
from app.models import TaskOutput

predictor = OpenAIPredictor(output_model=TaskOutput)

def generate_task(prompt: str) -> TaskOutput:
    return predictor.predict(prompt)