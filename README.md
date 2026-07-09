# Autonomous Multi-Step AI Agent

An autonomous AI agent built using **FastAPI**, **LangGraph**, **Google Gemini**, and **python-docx**. The agent accepts a natural language request, autonomously creates an execution plan, generates a structured business document section by section, performs quality validation using a reflection step, and exports the final result as a Microsoft Word (`.docx`) document.

---

# Features

* Autonomous task planning using an LLM
* Multi-step execution workflow with LangGraph
* Structured JSON output using Pydantic schemas
* Reflection (Self-Check) with bounded retries
* Automatic Microsoft Word (.docx) generation
* FastAPI REST API
* Download generated documents via API
* Request validation using Pydantic

---

# Architecture

```text
                User Request
                     │
                     ▼
              Planner Node
                     │
                     ▼
             Execution Plan
                     │
                     ▼
             Executor Node
                     │
                     ▼
            Reflection Node
          ┌──────────┴──────────┐
          │                     │
      Retry Section        Next Section
          │                     │
          └──────────┬──────────┘
                     ▼
          Document Generator
                     │
                     ▼
          Microsoft Word (.docx)
```

---

# Tech Stack

* Python 3.11+
* FastAPI
* LangGraph
* Google Gemini API
* Pydantic
* python-docx
* python-dotenv

---

# Project Structure

```text
.
├── app.py
├── graph.py
├── planner.py
├── executor.py
├── reflection.py
├── doc_generator.py
├── prompts.py
├── schemas.py
├── state.py
├── generated_docs/
├── requirements.txt
└── .env
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/<repository-name>.git

cd <repository-name>
```

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

# Run the Application

```bash
uvicorn app:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# API

## POST `/agent`

### Request

```json
{
  "request": "Create a business proposal for an AI-powered inventory management system."
}
```

### Sample Response

```json
{
  "rationale": "The document is organized into executive summary, project scope, implementation plan, budget, risks, and conclusion.",
  "assumptions_made": [
    "Project budget was not provided.",
    "Cloud deployment is assumed.",
    "Enterprise users are the target audience."
  ],
  "execution_log": [
    "Autonomous execution plan created.",
    "Generated Executive Summary.",
    "Quality Check Approved.",
    "Generated Implementation Plan.",
    "Quality Check Approved.",
    "Document exported successfully."
  ],
  "download_url": "/download/project_proposal.docx"
}
```

---

# Agent Workflow

### 1. Planning

The Planner node analyzes the user's request and generates a structured execution plan consisting of document sections and assumptions.

### 2. Execution

The Executor node generates one document section at a time while maintaining context from previously generated sections.

### 3. Reflection

Each generated section is reviewed by a dedicated reflection node.

If quality checks fail, the section is regenerated.

Reflection retries are limited to prevent infinite execution loops.

### 4. Document Generation

The final approved sections are converted into a professionally formatted Microsoft Word document.

---

# Engineering Improvement

## Reflection with Bounded Retries

This project implements **Reflection / Self-Check** as the primary engineering improvement.

After generating each section, the agent reviews it for:

* Professional quality
* Completeness
* Grammar
* Business value
* Placeholder content

If a section fails the quality check, the executor regenerates it.

To avoid infinite retry loops and excessive API usage, the workflow tracks reflection attempts and limits retries before proceeding with the best available version.

This improves robustness while maintaining autonomous behavior.

---

# Example Documents

The agent can generate:

* Business Proposal
* Project Plan
* Technical Design Document
* Product Specification
* Meeting Minutes
* Business Report
* Standard Operating Procedure (SOP)

---

# Future Improvements

* Multi-model fallback (Gemini, Groq, Ollama)
* Conversation Memory
* Retrieval-Augmented Generation (RAG)
* Tool Calling
* Persistent State Storage
* Docker Deployment
* Authentication & Authorization
* Streaming Responses

---

# Known Limitation

The current implementation uses the **Google Gemini Free Tier**. During extensive testing, the API may return:

* **429 RESOURCE_EXHAUSTED** (rate limit or daily quota exceeded)
* **503 UNAVAILABLE** (temporary service overload)

The workflow is designed so the underlying LLM provider can be replaced with another supported provider (such as Groq or Ollama) without changing the overall agent architecture.

---

# License

This project was developed for learning purposes and technical assessment demonstrations.
