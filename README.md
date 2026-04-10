# AI Meeting & Knowledge Assistant 🚀

Transform meeting recordings into persistent, searchable knowledge.

## 🏗️ Tech Stack
- **Backend**: FastAPI (Python)
- **AI**: Gemini 1.5 (Pro/Flash) for Audio Processing, Summarization, and RAG.
- **Database**: SQLAlchemy + SQLite
- **Vector Search**: FAISS
- **Frontend**: Next.js 14 + Vanilla CSS (Midnight Glassmorphism Theme)

## 🚀 Getting Started

### Backend Setup
1. Create a `.env` file in the `backend/` directory based on `.env.example`.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to `frontend/`:
   ```bash
   npm install
   ```
2. Run the development server:
   ```bash
   npm run dev
   ```

## 🧠 Core Features
- **Meeting Ingestion**: Upload audio files for automatic processing.
- **AI Insights**: Automated transcripts, summaries, action items, and decision logs.
- **Knowledge Search**: Query across all meetings using semantic search (RAG).
- **Premium Design**: Sleek "Midnight" theme with glassmorphism and smooth interactions.
