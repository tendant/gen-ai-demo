from fastapi import APIRouter
from app.models import TaskInput, TaskOutput
from app.services import generate_task

router = APIRouter()

@router.post("/generate", response_model=TaskOutput)
async def generate(data: TaskInput):
    return await generate_task(data.description)