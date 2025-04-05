from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import recognition

app = FastAPI(
    title="POS Image Recognition Microservice",
    description="Microservice for product image recognition"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(recognition.router, prefix="/api/recognition", tags=["Recognition"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}