from fastapi import FastAPI

from app.api.research import router as research_router
from app.api.sources import router as sources_router

app = FastAPI()
app.include_router(sources_router)
app.include_router(research_router)


@app.get("/")
async def root():
    return {"message": "Backend is running"}
