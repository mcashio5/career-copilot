import os
import secrets

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader

from ai import analyze
from models import AnalysisResult

app = FastAPI(title="Career Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_access(key: str | None):
    expected = os.environ.get("APP_PASSWORD")
    if not expected:
        return
    if key is None or not secrets.compare_digest(key, expected):
        raise HTTPException(status_code=401, detail="Invalid access key.")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    x_access_key: str | None = Header(default=None),
):
    check_access(x_access_key)

    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    reader = PdfReader(resume.file)
    resume_text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

    if len(resume_text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Couldn't read text from that PDF (is it a scanned image?).",
        )

    # Prevent extremely large job descriptions from being sent to the AI
    if len(job_description) > 50_000:
        raise HTTPException(
            status_code=400,
            detail="Job description is too long.",
        )

    return analyze(resume_text, job_description)

if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")