import json
import logging
import os
import shutil
from pathlib import Path

from typing import Any, Dict
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from config.config_loader import settings
from ocr.service import OCRService
from classify.service import ClassificationService
from agents.orchestrator_agent import DocumentOrchestratorAgent

logger = logging.getLogger("run")

# Instantiate Services
ocr_service = OCRService()
classify_service = ClassificationService()
orchestrator = DocumentOrchestratorAgent()

# Initialize FastAPI App
app = FastAPI(
    title=settings.yaml_config.get("app", {}).get("title", "Document Intelligence System"),
    version=settings.yaml_config.get("app", {}).get("version", "1.0.0"),
    description=settings.yaml_config.get("app", {}).get("description", ""),
)

# Set up CORS middleware for production-ready setups
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", tags=["General"])
def read_root():
    """Returns basic metadata about the Document Intelligence System."""
    return {
        "app": app.title,
        "version": app.version,
        "description": app.description,
        "environment": settings.env,
        "status": "online"
    }


@app.get("/health", tags=["General"], status_code=status.HTTP_200_OK)
def health_check():
    """Simple API health check endpoint."""
    return {
        "status": "healthy",
        "gemini_api_key_configured": bool(settings.gemini_api_key)
    }

@app.post("/api/v1/process", tags=["Processing"], status_code=status.HTTP_200_OK)
async def process_document_pipeline(file: UploadFile = File(...)):
        print("API ENDPOINT HIT")

        logger.info(
            f"Running full document intelligence pipeline for: {file.filename}"
        )

        dest_path = settings.input_path / str(file.filename)

        try:
            with open(dest_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        except Exception as e:

            logger.error(
                f"Failed to save uploaded file: {e}"
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save upload: {str(e)}"
            )

        try:

            pipeline_result = orchestrator.process_document(
                str(dest_path)
            )

        except Exception as e:

            print("ORCHESTRATOR ERROR")
            print(type(e))
            print(str(e))

            raise

        output_filename = (
            f"{Path(file.filename).stem}_result.json"
        )

        output_file_path = (
            settings.output_path / output_filename
        )

        try:

            with open(
                output_file_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    pipeline_result,
                    f,
                    indent=4
                )

        except Exception as e:

            logger.error(
                f"Failed writing output file: {e}"
            )

        return {
            "status": "success",
            "json_output": str(output_file_path),
            "results": pipeline_result
        }

if __name__ == "__main__":
    logger.info(f"Starting server in {settings.env} mode...")
    uvicorn.run(
        "run:app",
        host=settings.host,
        port=settings.port,
        reload=settings.env == "development"
    )
