# AI Document Intelligence Platform

An AI-powered document processing platform built using **Google ADK**, **Gemini 2.5 Flash**, **FastAPI**, **Streamlit**, **OCR**, **Entity Extraction**, and **PII Detection**.

The platform enables users to upload documents and automatically perform:

* OCR Text Extraction
* Document Classification
* Named Entity Recognition (NER)
* PII Detection
* JSON Output Generation

---

# Features

## OCR Processing

Extracts text from:

* PDF
* PNG
* JPG
* JPEG
* DOCX
* TXT

Supports:

* Digital PDFs
* Image-based documents
* Multi-page document processing

---

## Document Classification

Uses Gemini 2.5 Flash to classify uploaded documents.

Supported examples:

* Invoice
* Receipt
* Contract
* Other custom categories

Output includes:

* Category
* Confidence Score
* Classification Reasoning

---

## Entity Extraction

Automatically extracts important business entities:

* Invoice Number
* Customer Name
* Email Address
* Phone Number
* PAN Number
* Aadhaar Number
* Organization Name
* Address
* Amount
* Date

---

## PII Detection

Detects Personally Identifiable Information (PII):

* Names
* Email Addresses
* Phone Numbers
* PAN Numbers
* Aadhaar Numbers

Useful for compliance and privacy workflows.

---

## Unified JSON Output

Generates a structured JSON response containing:

* OCR Results
* Classification Results
* Extracted Entities
* PII Detection Results
* Metadata

Results are automatically stored inside:

```text
outputs/json/
```

---

# Frontend Dashboard

The project includes a modern Streamlit dashboard.

Features:

* Dark Theme UI
* File Upload Interface
* OCR Results Tab
* Classification Tab
* Entity Extraction Tab
* PII Detection Tab
* Full JSON Output Tab
* Download Analysis Button

---

# System Architecture

```text
Document Upload
       │
       ▼
 OCR Processing
       │
       ▼
Document Classification
       │
       ▼
 Entity Extraction
       │
       ▼
 PII Detection
       │
       ▼
 JSON Generation
       │
       ▼
 Result Download
```

---

# Repository Structure

```text
project1/
│
├── agents/
│   ├── base.py
│   ├── orchestrator_agent.py
│   ├── ocr_agent.py
│   ├── classify_agent.py
│   ├── chunking_agent.py
│
├── classify/
│   ├── entity_extractor.py
│   ├── pii_detector.py
│   ├── llm_classifier.py
│   ├── validator.py
│
├── config/
│   ├── config.yaml
│   ├── logging.yaml
│   ├── classification_prompts.yaml
│   ├── entity_extraction_prompts.yaml
│   ├── pii_detection_prompts.yaml
│
├── data/
│   ├── input/
│   └── processed/
│
├── frontend/
│   ├── app.py
│   └── styles.css
│
├── ocr/
│   ├── service.py
│   ├── pdf_reader.py
│   ├── text_cleaner.py
│
├── outputs/
│   └── json/
│
├── run.py
├── requirements.txt
└── README.md
```

---

# Technology Stack

## AI & Agents

* Google ADK
* Gemini 2.5 Flash

## Backend

* FastAPI
* Uvicorn

## Frontend

* Streamlit
* Custom CSS

## OCR

* PyMuPDF
* Tesseract OCR

## Configuration

* YAML
* Python Dotenv

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd project1
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
ENV=development
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

---

# Running the Backend

```bash
python run.py
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Running the Frontend

```bash
python -m streamlit run frontend/app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# API Endpoints

## Health Check

```http
GET /health
```

---

## OCR

```http
POST /api/v1/ocr
```

---

## Classification

```http
POST /api/v1/classify
```

---

## Full Processing Pipeline

```http
POST /api/v1/process
```

Returns:

```json
{
  "ocr_metadata": {},
  "classification": {},
  "extracted_entities": [],
  "pii_detection": {}
}
```

---

# Sample Workflow

1. Upload Document
2. OCR Extraction
3. Document Classification
4. Entity Extraction
5. PII Detection
6. JSON Generation
7. Download Analysis

---

# Current Capabilities

✅ OCR Processing

✅ Document Classification

✅ Entity Extraction

✅ PII Detection

✅ FastAPI Backend

✅ Streamlit Frontend

✅ JSON Export

✅ Gemini Integration

---

# Author

Pratyush Raj

AI Document Intelligence Platform
