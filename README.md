<h1 align="center">🚀 AI Document Intelligence Platform</h1>

<p align="center">
  Production-grade Multi-Agent AI System for OCR, Document Classification, Entity Extraction, PII Detection & Structured JSON Output
</p>

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Google-Gemini-orange?style=for-the-badge&logo=google"/>
  <img src="https://img.shields.io/badge/Multi-Agent%20Architecture-purple?style=for-the-badge"/>

</p>

---

<p align="center">
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=25&duration=3000&pause=1000&color=00C2FF&center=true&vCenter=true&width=800&lines=AI+Powered+Document+Processing;OCR+%2B+Classification+%2B+NER+%2B+PII+Detection;Multi-Agent+Architecture+with+Gemini+LLM;Production+Ready+FastAPI+%2B+Streamlit+System"/>
</p>

---

# 📌 Project Overview

AI Document Intelligence Platform is an **industry-level intelligent document processing system** designed to automate extraction, classification, analysis, and security validation of documents.

The platform processes:

✅ Invoices  
✅ Receipts  
✅ Contracts  
✅ Business Documents  
✅ Scanned PDFs  
✅ Images  
✅ Structured & Unstructured Documents  

The system uses a **multi-agent pipeline architecture** where each agent performs a dedicated task independently and returns structured results.

---

# ✨ Key Features

- 📄 OCR Extraction from PDF/Image/Documents  
- 🤖 LLM Based Document Classification using Gemini  
- 🏷 Named Entity Recognition (NER)  
- 🔐 Sensitive Data / PII Detection  
- 📊 Structured JSON Output Generation  
- ⚡ FastAPI Backend Processing Engine  
- 🎨 Interactive Streamlit Frontend Dashboard  
- 🧠 Multi-Agent Modular Architecture  
- 📂 Support for PDF / JPG / PNG / DOCX / TXT  
- 📥 JSON Download Support  
- 📝 Rule Based Validation Engine  

---

# 🏗 System Architecture

```text
                ┌─────────────────────────────┐
                │       Streamlit Frontend    │
                │ Upload + Dashboard + Tabs   │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │       FastAPI Backend       │
                │        API Layer            │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │ Master Document Orchestrator│
                │      Pipeline Controller    │
                └──────────────┬──────────────┘
                               │
      ┌────────────────────────┼────────────────────────┐
      │                        │                        │
      ▼                        ▼                        ▼

┌─────────────┐        ┌──────────────┐        ┌──────────────┐
│ OCR Agent   │        │ Chunk Agent  │        │ Rule Engine  │
│ PyMuPDF +   │        │ Page Chunking│        │ Regex Engine │
│ Tesseract   │        │              │        │              │
└──────┬──────┘        └──────┬───────┘        └──────────────┘
       │                      │
       ▼                      ▼

        ┌─────────────────────────────────────┐
        │      Extracted Document Text        │
        └─────────────────────────────────────┘
                             │
                             ▼

                 ┌───────────────────────┐
                 │ Gemini Classification │
                 │ Invoice / Receipt etc │
                 └──────────┬────────────┘
                            │
                            ▼

                 ┌───────────────────────┐
                 │ Entity Extraction     │
                 │ NER Processing        │
                 └──────────┬────────────┘
                            │
                            ▼

                 ┌───────────────────────┐
                 │ PII Detection Agent   │
                 │ PAN/Aadhaar/Email     │
                 └──────────┬────────────┘
                            │
                            ▼

                 ┌───────────────────────┐
                 │ Validation Engine     │
                 │ Rule Verification     │
                 └──────────┬────────────┘
                            │
                            ▼

                 ┌───────────────────────┐
                 │ JSON Report Generator │
                 └──────────┬────────────┘
                            │
                            ▼

                 ┌───────────────────────┐
                 │ Final Structured JSON │
                 └───────────────────────┘
```

---

# ⚙ Processing Pipeline

```text
User Upload
      │
      ▼
OCR Extraction
      │
      ▼
Page Chunking
      │
      ▼
Rule Classification
      │
      ▼
Gemini LLM Classification
      │
      ▼
Entity Extraction (NER)
      │
      ▼
PII Detection
      │
      ▼
Validation Engine
      │
      ▼
JSON Output Generation
      │
      ▼
Frontend Display + Download
```

---

# 🧠 Multi-Agent Workflow

### 1. OCR Agent

Responsible for extracting document text.

Uses:

- PyMuPDF (Digital PDFs)
- Tesseract OCR (Scanned PDFs)

---

### 2. Chunking Agent

Splits document page-wise for efficient processing.

Purpose:

- Reduce token usage
- Page-level analysis
- Faster processing

---

### 3. Rule Classification Agent

Uses regex-based logic.

Detects:

- Invoice patterns
- PAN patterns
- Date patterns
- Structured fields

---

### 4. Gemini LLM Classification Agent

Uses Gemini API.

Classifies documents into:

- Invoice
- Receipt
- Contract
- Other

Returns:

- Category
- Confidence
- Reasoning

---

### 5. Entity Extraction Agent

Performs Named Entity Recognition.

Extracts:

- Person Name
- Email
- Phone Number
- PAN Number
- Aadhaar Number
- Organization
- Invoice Number
- Amount
- Date

---

### 6. PII Detection Agent

Detects sensitive information.

Includes:

- PAN Card
- Aadhaar Number
- Email
- Phone Number
- Personal Information

---

### 7. Validation Agent

Performs format validation.

Checks:

- Aadhaar structure
- PAN regex
- Email format
- Numeric validation

---

### 8. JSON Generator

Combines all agent outputs into unified JSON.

---

# 🖥 Frontend Dashboard

Frontend built using **Streamlit**.

Features:

- Upload documents
- Start processing
- OCR output tab
- Classification tab
- Entity extraction tab
- PII detection tab
- JSON output tab
- Download analysis button

---

# 📂 Project Structure

```bash
project1/
│
├── agents/
│   ├── base.py
│   ├── orchestrator_agent.py
│   ├── chunking_agent.py
│   ├── ocr_agent.py
│
├── classify/
│   ├── llm_classifier.py
│   ├── entity_extractor.py
│   ├── pii_detector.py
│   ├── validator.py
│
├── ocr/
│   ├── pdf_reader.py
│   ├── service.py
│   ├── tesseract_engine.py
│
├── frontend/
│   └── app.py
│
├── config/
│   ├── config.yaml
│   ├── logging.yaml
│   ├── classification_prompts.yaml
│
├── data/
│   └── input/
│
├── outputs/
│   └── json/
│
├── run.py
│
└── requirements.txt
```

---

# 🛠 Tech Stack

### Backend

- FastAPI
- Uvicorn
- Python 3.12

### Frontend

- Streamlit
- HTML/CSS

### AI Layer

- Google Gemini API
- Google ADK

### OCR Layer

- PyMuPDF
- Tesseract OCR

### Processing

- Regex
- JSON Processing
- Multi-Agent Workflow

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Pratyushr949/intelligent-document-processing.git
```

```bash
cd intelligent-document-processing
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
.\venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure API Key

Create `.env`

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
ENV=development
HOST=0.0.0.0
PORT=8000
```

---

# ▶ Run Backend

```bash
python run.py
```

Runs on:

```text
http://localhost:8000
```

---

# ▶ Run Frontend

```bash
python -m streamlit run frontend/app.py
```

Runs on:

```text
http://localhost:8501
```

---

# Sample JSON Output

```json
{
  "classification": {
      "category":"Invoice",
      "confidence":0.99
  },

  "entities":[
      {
        "type":"Email",
        "value":"john@example.com"
      }
  ],

  "pii_detection":{
      "pii_entities":[
          {
             "type":"PAN Number",
             "value":"ABCDE1234F"
          }
      ]
  }
}
```

---

# Future Improvements

- Parallel Agents using Ray
- JWT Authentication
- Batch PDF Processing
- Database Integration
- Human Review Workflow
- Audit Logging
- Confidence Formula Calculation
- Docker Deployment
- Vector Database Integration

---

# Performance Goals

- Low Latency Processing  
- Scalable Agent Architecture  
- Structured JSON Generation  
- Modular Codebase  
- Production Ready Backend  

---

# Developed By

### Pratyush Raj

AI/ML Engineer | Multi-Agent Systems | Document Intelligence | LLM Engineering

GitHub:

https://github.com/Pratyushr949

---

<p align="center">

<img src="https://github-profile-trophy.vercel.app/?username=Pratyushr949&theme=algolia"/>

</p>

---

<p align="center">

⭐ If you like this project, give it a star.

</p>
