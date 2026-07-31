from fastapi import FastAPI

app = FastAPI(title="Career Copilot API")


@app.get("/api/health")
def health():
    return {"status": "ok"}