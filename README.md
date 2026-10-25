# GeneratorJam ✨

**AI-powered content creation for your social media.**
Generate blog posts, tweets, Instagram captions and LinkedIn posts with Google Gemini, create images with Hugging Face models, and keep everything in a searchable history you can copy, download, favourite or delete.

[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-38BDF8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)

🔗 **Demo:** https://generatorjam.onrender.com *(hosted on a free tier, so the first load can take a few seconds)*

---

## Features

- **Text generation** for four formats: blog post, Twitter/X, Instagram caption, LinkedIn post. Each format uses its own writing prompt, powered by Gemini (`gemini-2.0-flash-lite`).
- **Image generation** through the Hugging Face Inference API. If one model fails, the backend automatically falls back to the next: FLUX.1-dev → FLUX.1-schnell → SDXL → Stable Diffusion 3.5 Large.
- **History** of every generation, stored in MongoDB per user.
- **Quick actions:** copy to clipboard, download, mark as favourite, delete one item, or clear all.
- **Friendly UX:** toast notifications for success, errors and offline state; responsive layout built with shadcn/ui + Radix.

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Tailwind CSS, shadcn/ui (Radix UI), Axios, CRACO |
| Backend | Python, FastAPI, Pydantic, Motor (async MongoDB) |
| AI | Google Gemini API, Hugging Face Inference API |
| Database | MongoDB |

## API

All routes are prefixed with `/api`. Requests are scoped to a user through a `user_id` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate/text` | Generate text for a given prompt and content type |
| `POST` | `/generate/image` | Generate an image from a prompt |
| `GET` | `/history` | List the user's generation history |
| `PUT` | `/history/{item_id}/favorite` | Toggle favourite on an item |
| `DELETE` | `/history/{item_id}` | Delete one history item |
| `DELETE` | `/history` | Clear the whole history |
| `GET` | `/health` | Health check |

Interactive docs are available at `http://localhost:8000/docs` when the backend is running.

## Getting started

### Prerequisites

- Node.js 18+ and npm (or Yarn)
- Python 3.10+
- A MongoDB instance (local or MongoDB Atlas)
- A [Gemini API key](https://aistudio.google.com/app/apikey) and a [Hugging Face access token](https://huggingface.co/settings/tokens)

### 1. Clone

```bash
git clone https://github.com/Deep9873/GeneratorJam.git
cd GeneratorJam
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your values
uvicorn server:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm start
```

The app opens at `http://localhost:3000`.

## Environment variables

**`backend/.env`**

| Variable | Description |
|----------|-------------|
| `MONGO_URL` | MongoDB connection string |
| `DB_NAME` | Database name |
| `GEMINI_API_KEY` | Google Gemini API key (required) |
| `HF_TOKEN` | Hugging Face access token (required) |

**`frontend/.env`**

| Variable | Description |
|----------|-------------|
| `REACT_APP_BACKEND_URL` | Base URL of the backend, e.g. `http://localhost:8000` |

> 🔐 Never commit real keys. `.env` files are listed in `.gitignore`; use the provided `.env.example` files as templates.

## Project structure

```text
GeneratorJam/
├── backend/
│   ├── server.py                  # FastAPI app and routes
│   ├── models.py                  # Pydantic request/response models
│   ├── services/
│   │   ├── gemini_service.py      # Text generation (Gemini)
│   │   └── huggingface_service.py # Image generation with model fallback
│   └── requirements.txt
├── frontend/
│   ├── public/
│   └── src/components/
│       ├── GeneratorJam.jsx       # Main generator + history UI
│       └── ui/                    # shadcn/ui components
└── backend_test.py                # API tests
```

## Author

**Deep Jangid** · [@Deep9873](https://github.com/Deep9873)

