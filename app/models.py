from pydantic import BaseModel

class TaskInput(BaseModel):
    description: str

class TaskOutput(BaseModel):
    output: str
