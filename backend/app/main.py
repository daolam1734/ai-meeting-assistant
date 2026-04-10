import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

from .models.db_config import init_db, get_db
from .models.database import Meeting, Task, Decision
from .services.intelligence import IntelligenceService
from .services.vector_store import VectorStoreService

app = FastAPI(title="AI Meeting Assistant API")

# Initialize DB
init_db()

# Services
intel_service = IntelligenceService(api_key=os.getenv("GOOGLE_API_KEY", ""))
vector_service = VectorStoreService(api_key=os.getenv("GOOGLE_API_KEY", ""))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Meeting Assistant API is running"}

@app.post("/upload")
async def upload_meeting(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Process with Gemini
        meta = await intel_service.process_audio(temp_path)
        
        # 3. Save to DB
        meeting = Meeting(
            title=file.filename.split('.')[0],
            transcript=meta.get("transcript", ""),
            summary=meta.get("summary", "")
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        
        # 4. Save Tasks and Decisions
        for t in meta.get("action_items", []):
            task = Task(content=t if isinstance(t, str) else t.get("task", ""), meeting_id=meeting.id)
            db.add(task)
            
        for d in meta.get("decisions", []):
            decision = Decision(content=d if isinstance(d, str) else d.get("decision", ""), meeting_id=meeting.id)
            db.add(decision)
            
        db.commit()
        
        # 5. Index in Vector Store
        vector_service.add_meeting_transcript(meeting.id, meeting.transcript)
        
        return {
            "id": meeting.id,
            "title": meeting.title,
            "summary": meeting.summary,
            "tasks_count": len(meta.get("action_items", [])),
            "decisions_count": len(meta.get("decisions", []))
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/meetings")
async def get_meetings(db: Session = Depends(get_db)):
    meetings = db.query(Meeting).order_by(Meeting.date.desc()).all()
    return meetings

@app.get("/meetings/{meeting_id}")
async def get_meeting_detail(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "id": meeting.id,
        "title": meeting.title,
        "date": meeting.date,
        "transcript": meeting.transcript,
        "summary": meeting.summary,
        "tasks": [t.content for t in meeting.tasks],
        "decisions": [d.content for d in meeting.decisions]
    }

@app.get("/search")
async def search_knowledge(query: str):
    results = vector_service.search_knowledge(query)
    return [
        {"content": r.page_content, "metadata": r.metadata}
        for r in results
    ]
