from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pypdf import PdfReader

from ai import analyze
from models import AnalysisResult

app = FastAPI(title="Career Copilot API")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
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

    return analyze(resume_text, job_description)
