# 🚀 ConsensusDoc AI — Multi-Agent Intelligent Document Processing Platform

> **Enterprise-grade AI Document Intelligence Platform powered by Multi-Agent Consensus Architecture, Google ADK, Gemini, Ray Parallel Processing, OCR, Human-in-the-Loop Validation, and Automated Structured Output Generation.**

---

## 🌟 Project Overview

**ConsensusDoc AI** is an advanced **Intelligent Document Processing (IDP)** platform designed to automate enterprise document understanding workflows.

Unlike traditional single-model pipelines, this system uses **multiple AI agents running in parallel** to independently classify and analyze uploaded documents.

The system then performs **consensus-based voting**, calculates a **mathematical confidence score**, and automatically routes uncertain predictions for **human review**.

The platform is designed to simulate **industry-grade enterprise document automation systems** used in:

* Banking
* Insurance
* FinTech
* KYC Verification
* Compliance Automation
* Enterprise Document Intelligence

---

# 🔥 Core Innovation

Instead of relying on a single AI model:

```text
Traditional Systems

PDF → Single Model → Output
```

ConsensusDoc AI uses:

```text
ConsensusDoc AI

PDF
 ↓
OCR Extraction
 ↓
Preprocessing Engine
 ↓
5 Parallel AI Agents (Ray Distributed Execution)

Agent 1
Agent 2
Agent 3
Agent 4
Agent 5

 ↓

Consensus Voting Engine

 ↓

Confidence Calculation Engine

 ↓

Threshold Decision Engine

High Confidence → JSON + Excel Output

Low Confidence → Human Review Queue
```

This significantly improves:

* Reliability
* Accuracy
* Explainability
* Fault Tolerance
* Decision Confidence

---

# 🏗 System Architecture

```text
User Upload PDF / Document
            │
            ▼
      OCR Extraction Engine
        (PaddleOCR)

            │
            ▼
      Text Preprocessing
   (Cleaning + Normalization)

            │
            ▼
      Ray Parallel Execution

 ┌─────────────────────────────────┐
 │      Multi-Agent Layer         │
 │                               │
 │  Agent 1 → Document Classifier │
 │  Agent 2 → Document Classifier │
 │  Agent 3 → Document Classifier │
 │  Agent 4 → Document Classifier │
 │  Agent 5 → Document Classifier │
 │                               │
 └─────────────────────────────────┘

            │
            ▼
      Consensus Voting Engine

            │
            ▼
     Confidence Score Engine

 Formula:

 FinalConfidence =
 VoteRatio × AverageConfidence × (1 - Variance)

            │
            ▼

   ┌─────────────────────┐
   │ Threshold ≥ 0.75    │
   │                     │
   │ Generate Outputs    │
   └─────────────────────┘

            │

   ┌─────────────────────┐
   │ Threshold < 0.75    │
   │                     │
   │ Human Review Queue  │
   └─────────────────────┘

            │
            ▼

 Structured JSON + Excel Output
```

---

# ⚡ Key Features

## 📄 OCR Processing Engine

Extracts text from:

* PDF
* Scanned PDFs
* Multi-page documents
* Image-based documents

Powered by:

* PaddleOCR
* pdfplumber
* NumPy

Capabilities:

* High accuracy OCR extraction
* Multi-page PDF support
* Scanned document support

---

## 🤖 Parallel Multi-Agent AI System

Uses **5 AI Agents running simultaneously** using **Ray distributed execution**.

Each agent independently analyzes the same document.

Benefits:

* Parallel inference
* Independent reasoning
* Higher reliability
* Fault tolerance
* Consensus-based decision making

---

## 🧠 Google ADK + Gemini Integration

Built using:

* Google ADK
* Gemini 2.5 Flash

Capabilities:

* Document understanding
* Semantic classification
* JSON structured responses
* Classification reasoning generation

---

## 🗳 Consensus Voting Engine

Each agent independently predicts:

Example:

```text
Agent 1 → invoice → 0.95

Agent 2 → invoice → 0.97

Agent 3 → passport → 0.85

Agent 4 → invoice → 0.92

Agent 5 → invoice → 0.98
```

Voting Engine decides:

```text
Final Document Type = Invoice
```

Benefits:

* Reduced hallucination
* Improved accuracy
* Better reliability

---

## 📊 Mathematical Confidence Engine

Confidence score is NOT blindly taken from the LLM.

Instead:

```text
FinalConfidence = VoteRatio × AverageConfidence × (1 - Variance)
```

This provides:

* Mathematical reliability scoring
* Lower hallucination risk
* Better confidence estimation

---

## 👨 Human-in-the-Loop Review System

If confidence falls below threshold:

```text
Threshold < 0.75
```

The document is automatically sent to:

```text
storage/review_queue/
```

Benefits:

* Manual verification
* Safer enterprise deployment
* Reduced wrong classifications

---

## 📁 Automated Output Generation

System automatically generates:

### JSON Output

```text
storage/json/
```

Contains:

* Document Type
* Confidence Score
* Agent Predictions
* Consensus Result
* Reasoning

---

### Excel Output

```text
storage/excel/
```

Contains:

* Classification Summary
* Confidence Metrics
* Agent-wise Results
* Final Decision

---

# 📌 Supported Document Types

Currently supports classification of:

* Invoice
* Passport
* Aadhaar
* PAN Card
* Bank Statement
* Insurance Document

Architecture supports future expansion.

---

# 🛠 Technology Stack

## AI & LLM Layer

* Google ADK
* Gemini 2.5 Flash

## Parallel Processing

* Ray Distributed Computing

## Backend

* FastAPI
* Uvicorn

## OCR

* PaddleOCR
* pdfplumber
* NumPy

## Data Processing

* Pandas
* JSON
* OpenPyXL

## Configuration

* YAML
* Python Dotenv

## Future Frontend

* React
* Vite
* Tailwind CSS
* Recharts
* Framer Motion

---

# 📂 Project Structure

```text
project2/

├── agents/
│   ├── adk_agent_1.py
│   ├── adk_agent_2.py
│   ├── adk_agent_3.py
│   ├── adk_agent_4.py
│   ├── adk_agent_5.py
│   └── ray_manager.py
│
├── backend/
│   ├── orchestrator.py
│   ├── ocr_engine.py
│   ├── preprocess.py
│   ├── confidence_engine.py
│   ├── confidence_threshold.py
│   ├── voting_engine.py
│   ├── reason_aggregator.py
│   ├── json_generator.py
│   ├── excel_generator.py
│   └── routes.py
│
├── config/
│   ├── config.yaml
│   └── key_manager.py
│
├── storage/
│   ├── json/
│   ├── excel/
│   └── review_queue/
│
├── run.py
├── requirements.txt
└── README.md
```

---

# 🌐 API Endpoints

### Health Check

```http
GET /health
```

### Upload Document

```http
POST /api/upload
```

### View Documents

```http
GET /api/documents
```

### Review Queue

```http
GET /api/review-queue
```

### Download JSON Output

```http
GET /api/documents/{doc_id}/download/json
```

### Download Excel Output

```http
GET /api/documents/{doc_id}/download/excel
```

---

# 📈 Current Development Status

Backend Progress:

```text
OCR Engine                 ✅ Completed

FastAPI Backend           ✅ Completed

Parallel Ray Agents       ✅ Completed

Google ADK Integration    ✅ Completed

Consensus Engine          ✅ Completed

Confidence Engine         ✅ Completed

Human Review Queue        ✅ Completed

JSON Generation           ✅ Completed

Excel Generation          ✅ Completed

Frontend Dashboard        🚧 In Progress

Authentication Layer      🚧 Planned
```

---

# 🎯 Future Improvements

Planned upgrades:

* Enterprise React Frontend Dashboard
* JWT Authentication
* Admin/User Login System
* PostgreSQL Database
* Real-time Analytics Dashboard
* Agent Performance Monitoring
* Document History Tracking
* Production Deployment

---

# 👨‍💻 Author

**Pratyush Raj**

B.Tech CSE (AI/ML)

Building enterprise-grade AI systems focused on:

* Multi-Agent AI
* Document Intelligence
* Distributed AI Systems
* Production AI Engineering

---

# ⭐ Project Vision

Building an enterprise-grade **Intelligent Document Processing Platform** that combines:

* Multi-Agent AI Systems
* Distributed Parallel Computing
* Consensus Decision Intelligence
* Human-in-the-Loop Validation
* Reliable AI Confidence Estimation

to create **trustworthy production-ready AI systems**.
