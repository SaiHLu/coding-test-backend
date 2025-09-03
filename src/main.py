from fastapi import FastAPI
from .routers import company

app = FastAPI()


@app.get("/health-check")
async def health_check():
    return {"status": "healthy"}


app.include_router(company.router, prefix="/companies", tags=["companies"])
