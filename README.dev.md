# Autolinker Developer Guide

This document contains developer setup instructions for the Autolinker full-stack application.

---

## 🔧 Tech Stack

- **Frontend**: React + TypeScript
- **Backend**: FastAPI (Python 3.10+)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Embeddings & AI**: OpenAI Embedding API + GPT-4
- **Deployment**: Render (Free tier)
- **Storage**: Supabase Tables

---

## 🗂 Folder Structure

```
autolinker_with_env/
├── backend/          # FastAPI server
├── frontend/         # React UI
├── render.yaml       # Render deployment config
├── .env.example      # Reference for local setup
├── README.md         # Production overview
├── README.dev.md     # This file (dev guide)
```

---

## 🚀 Local Development

### ✅ Prerequisites

- Node.js 16+ and `npm`
- Python 3.10+ and `pip`
- (Optional) `virtualenv` or `venv` for isolation

---

## ⚙️ Setup Instructions

### 📁 Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # .venv\Scripts\activate on Windows
pip install -r requirements.txt
python import_nltk.py            # Downloads NLTK punkt tokenizer
cp ../.env.example .env          # Create .env manually with real keys
```

To run locally:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 📁 Frontend

```bash
cd frontend
npm install
cp ../.env.example .env          # Create frontend .env
```

To run:
```bash
npm start
```

> React app runs at `http://localhost:3000`

---

## 🔐 Environment Variables

Create your `.env` files:

**backend/.env**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_api_key
FRONTEND_ORIGIN=http://localhost:3000
```

**frontend/.env**
```env
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 🧪 Test the App

1. Start both backend and frontend
2. Go to `http://localhost:3000`
3. Submit a blog URL (e.g., from jaanlabs.com or celf.beauty)
4. See progress page and anchor suggestions after GPT analysis

---

## 🛠️ Developer Notes

- `pipeline.py` runs the entire process:
  1. Crawl blog posts
  2. Extract + clean content
  3. Embed using OpenAI
  4. Match blog embeddings
  5. Suggest anchor links using GPT-4
- NLTK's `punkt` tokenizer is required at runtime
- Supabase stores blogs and their embeddings in a `blogs` table
- Backend is warmed up via `/api/ping` to avoid Render cold starts

---

## 🔁 Deployment (Render)

Configured via `render.yaml`.

- Frontend → Static Site
- Backend → Web Service

### ✅ Environment Variables (on Render)

**Backend**
```env
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
OPENAI_API_KEY=...
FRONTEND_ORIGIN=https://autolinker-frontend.onrender.com
```

**Frontend**
```env
REACT_APP_API_URL=https://autolinker-backend.onrender.com/api
```

---

## 🧠 Project Management

- See `PRD & Project Plan - Autolinker.pdf` for scope
- Prompt-based GPT + embedding system
- pgvector + cosine similarity used for semantic blog matching
- Results include anchor text + sentence suggestions

---

## 🧑‍💻 Contributors

- Project Owner: NikhilNagaich
- Prompt Designer: GPT-4
- AI Dev Partner: Code Copilot 🤖

Pull requests welcome! 💬
