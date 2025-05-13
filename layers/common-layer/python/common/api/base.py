from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from aws_lambda_powertools import Logger
from typing import Optional, Dict, Any
import json
import os

# Initialize logger
logger = Logger(service="api")

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="SDIMS API",
        description="Internal Management System API",
        version="1.0.0",
        docs_url="/api/docs" if os.getenv("ENVIRONMENT") != "prod" else None,
        redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") != "prod" else None
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=json.loads(os.getenv("ALLOWED_ORIGINS", '["*"]')),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # Log request
        logger.info(f"Request started", extra={
            "path": request.url.path,
            "method": request.method,
            "client_host": request.client.host if request.client else None
        })
        
        response = await call_next(request)
        
        # Log response
        logger.info(f"Request completed", extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code
        })
        
        return response
    
    return app

# Create FastAPI instance
app = create_app()

# Create Lambda handler
handler = Mangum(app, api_gateway_base_path="/api/v1") 