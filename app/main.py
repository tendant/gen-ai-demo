# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Then import FastAPI and other modules
from fastapi import FastAPI
from app.routes import router

app = FastAPI()
app.include_router(router)
