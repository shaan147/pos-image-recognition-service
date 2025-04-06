from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from src.routes import recognition
from src.config.database import db_connection
from contextlib import asynccontextmanager
from src.config.settings import settings
# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database and log details
    try:
        # Try to ping the database
        db_connection.client.admin.command('ping')
        print(f"Connected to MongoDB: {db_connection.database.name}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
    
    yield  # This line separates startup from shutdown events
    
    # Shutdown: Close database connections
    try:
        db_connection.close_connection()
        print("Database connections closed")
    except Exception as e:
        print(f"Error closing database connection: {str(e)}")

# Create FastAPI app with lifespan handler
app = FastAPI(
    title="POS Image Recognition Microservice",
    description="Microservice for product image recognition",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan  # Add the lifespan handler here
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(recognition.router, prefix="/api/recognition", tags=["Recognition"])

@app.get("/health")
def health_check():
    """
    Health check endpoint with database status
    
    Returns:
        dict: Service health status
    """
    try:
        # Try to ping the database
        db_connection.client.admin.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy", 
        "version": "1.0.0",
        "database": {
            "status": db_status,
            "name": db_connection.database.name
        }
    }

# Custom Swagger UI with authentication
@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Documentation",
        swagger_favicon_url="/favicon.ico",
    )
@app.get("/debug/db")
def debug_database():
    """
    Debug endpoint to show database details
    """
    # Settings value
    settings_db_name = settings.DATABASE_NAME
    
    # Connection from database.py
    db_connection_name = db_connection.database.name
    
    # Recognition engine database
    recog_engine_db_name = recognition.recognition_engine.db.name
    
    return {
        "settings_db_name": settings_db_name,
        "db_connection_name": db_connection_name,
        "recog_engine_db_name": recog_engine_db_name,
        "available_databases": db_connection.client.list_database_names(),
        "connection_uri": settings.MONGODB_URI
    }