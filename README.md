# Document Intelligence System

A production-ready Python project skeleton designed for processing, classifying, and extracting information from documents (invoices, receipts, contracts, etc.) using the **Google Agent Development Kit (ADK)**, **Gemini API**, and **FastAPI**.

This project provides a clean, modular, code-first architecture designed to scale. It avoids containing concrete business logic but implements a complete routing, logging, environment configuration, and agent instantiation structure.

---

## Architecture & Repository Structure

The project directory contains the following layout:

```
├── config/
│   ├── config.yaml          # YAML application configuration (models, default settings)
│   ├── logging.yaml         # Python rotating logging configuration (dictConfig format)
│   └── config_loader.py     # Environment variable (.env) and config.yaml merging loader
├── data/
│   ├── input/               # Uploaded raw document files directory
│   └── processed/           # Temporary/intermediate processed data files directory
├── ocr/
│   ├── __init__.py
│   └── service.py           # OCR Service skeleton wrapping the DocumentOCRAgent
├── classify/
│   ├── __init__.py
│   └── service.py           # Classification Service skeleton wrapping the DocumentClassifyAgent
├── agents/
│   ├── __init__.py          # Exposed agent exports
│   ├── base.py              # BaseAgent (derived from Google ADK Agent)
│   ├── ocr_agent.py         # Subclass for Gemini OCR capabilities
│   └── classify_agent.py    # Subclass for Gemini Document Classification capabilities
├── outputs/
│   └── json/                # Directory for storing completed pipeline JSON results
├── venu/                    # Target custom virtual environment directory
├── .env.example             # Template for API credentials and network configurations
├── .env                     # Local environment settings (ignored from git tracking)
├── requirements.txt         # Project package requirements list
└── run.py                   # FastAPI application bootstrap and pipeline orchestrator
```

---

## Core Technologies Used

1. **Google ADK (Agent Development Kit)**: High-level code-first framework used to construct and execute AI agents (`google-adk`).
2. **Gemini API**: Orchestrates Gemini models (like `gemini-2.5-flash`) for multi-modal document reasoning.
3. **FastAPI**: Provides a modern, high-performance web interface to trigger agent tasks.
4. **Uvicorn**: Asynchronous ASGI server to run FastAPI.
5. **PyYAML & python-dotenv**: Manages application parameters and environment secrets.

---

## Getting Started

### 1. Prerequisite Environment Setup

Create and activate your Python virtual environment inside the requested directory:

```bash
# Create the virtual environment in venu/ directory
python -m venv venu

# Activate the virtual environment
# On Windows (Command Prompt / Powershell):
.\venu\Scripts\activate
# On macOS/Linux:
source venu/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Duplicate `.env.example` as `.env` and fill in your Gemini API key:

```env
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
ENV=development
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

Modify `config/config.yaml` if you need to alter default model variables, input/output paths, or classification categories.

### 3. Running the Server

Start the FastAPI application by executing `run.py`:

```bash
python run.py
```

The service will boot on `http://localhost:8000`. You can access the interactive Swagger documentation UI at `http://localhost:8000/docs`.

---

## API Endpoints Reference

### General Endpoints

*   **`GET /`**: Returns system information and environment state.
*   **`GET /health`**: Returns system health status and checks Gemini configurations.

### Processing Endpoints

*   **`POST /api/v1/classify`**:
    *   **Description**: Receives a document, uploads it to `data/input/`, and triggers `DocumentClassifyAgent`.
    *   **Payload**: `multipart/form-data` with key `file`.
*   **`POST /api/v1/ocr`**:
    *   **Description**: Receives a document, uploads it, and triggers `DocumentOCRAgent` to extract text contents.
    *   **Payload**: `multipart/form-data` with key `file`.
*   **`POST /api/v1/process`**:
    *   **Description**: Full pipeline execution. Saves the document to input directory, runs classification, runs OCR text extraction, generates a combined JSON output, saves the JSON to `outputs/json/<filename>_result.json`, and returns the payload.
    *   **Payload**: `multipart/form-data` with key `file`.
