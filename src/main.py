from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from .routers import company, waste, ai

app = FastAPI()

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"Origins: {origins}")


@app.get("/health-check", tags=["health"])
async def health_check():
    return {"status": "healthy"}


app.include_router(company.router, prefix="/companies", tags=["companies"])
app.include_router(waste.router, prefix="/wastes", tags=["wastes"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
