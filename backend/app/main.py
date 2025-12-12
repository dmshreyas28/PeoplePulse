"""PeoplePulse FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from .config import get_settings
from .db import engine, Base
from .routers import predict_router, simulate_router, employees_router
from .services import get_model_service, get_shap_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting PeoplePulse application...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    # Load ML model
    try:
        model_service = get_model_service(settings.model_path)
        if model_service.model is not None:
            logger.info("ML model loaded successfully")
            
            # Initialize SHAP service
            get_shap_service(model_service.model)
            logger.info("SHAP service initialized")
        else:
            logger.warning("ML model not found. Prediction endpoints may not work.")
    except Exception as e:
        logger.error(f"Failed to load ML model: {str(e)}")
        logger.warning("Application starting without ML model. Train and place model at: " + settings.model_path)
    
    yield
    
    # Shutdown
    logger.info("Shutting down PeoplePulse application...")


# Create FastAPI app
app = FastAPI(
    title="PeoplePulse API",
    description="Employee Attrition Prediction & Retention Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict_router)
app.include_router(simulate_router)
app.include_router(employees_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to PeoplePulse API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_service = get_model_service()
    
    return {
        "status": "healthy",
        "model_loaded": model_service.model is not None,
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
