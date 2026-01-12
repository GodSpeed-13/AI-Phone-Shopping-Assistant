# AI Phone Shopping Assistant (RAG-Based)

An API-first **Retrieval-Augmented Generation (RAG)** system that helps users
**discover, compare, and understand mobile phones** using structured retrieval
and controlled LLM generation.

This project focuses on **correct system design**, not just chatbot behavior:
deterministic retrieval, hard constraints, domain safety, and a stable API contract.

---

## 🚀 Setup Instructions

### Prerequisites
- Python **3.10+**
- Git
- A valid **Groq API key** or any other llm key

### Clone the Repository
```bash
git clone https://github.com/GodSpeed-13/AI-Phone-Shopping-Assistant.git
cd AI-Phone-Shopping-Assistant
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ `.env` is ignored via `.gitignore` and must never be committed.

### Run the Application
```bash
uvicorn app.main:app --reload
```

Open in browser:
```
http://127.0.0.1:8000
```

---

## 🧠 Tech Stack & Architecture Overview

### Backend
- **FastAPI**
- **FAISS**
- **Sentence Transformers**
- **Groq (LLaMA 3.3 70B)**

### Frontend
- HTML / CSS / Vanilla JavaScript
- Glassmorphism UI
- Responsive card-based layout

### Architecture Flow
```
User Query
   ↓
Safety & Domain Guard
   ↓
Intent Extraction
   ↓
Retriever (Hard Filters + FAISS)
   ↓
LLM Language Generator
   ↓
Canonical Response Builder
   ↓
UI Renderer
```

---

## 🧪 Prompt Design & Safety Strategy

### Prompt Design
- Structured prompts for intent extraction and response generation
- JSON-only outputs where required
- Low temperature for deterministic behavior

### Safety
- Domain restricted to mobile phones
- Blocks prompt injection, system prompt access, and secrets

---

## ⚠️ Known Limitations

- Static phone dataset
- No real-time pricing
- Embeddings require rebuild on data change
- No multi-turn memory
- No pagination in UI

---

## 👤 Author

**GodSpeed-13**
