from fastapi import FastAPI
from src.api.endpoints import router

app = FastAPI(
    title="World Ingestion & Systems Analysis Platform",
    description="A conversational platform for systems thinking analysis with MermaidJS diagrams",
    version="0.1.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)