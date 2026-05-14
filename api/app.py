"""MIRROR FastAPI application."""
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from core.orchestrator import run_pipeline

app = FastAPI(title="MIRROR", description="60 seconds of voice into 50 pieces of content.")

UPLOAD_DIR = Path("/tmp/mirror_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

_jobs: dict = {}


@app.get("/")
def root():
    return {"status": "ok", "service": "MIRROR"}


@app.post("/generate")
async def generate(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Accept an audio file and start the MIRROR pipeline in the background."""
    job_id = str(uuid.uuid4())[:8]
    audio_path = UPLOAD_DIR / f"{job_id}_{file.filename}"

    content = await file.read()
    audio_path.write_bytes(content)

    _jobs[job_id] = {"status": "running", "result": None, "error": None}

    def _run():
        try:
            result = run_pipeline(str(audio_path), user_id=job_id)
            _jobs[job_id] = {"status": "complete", "result": result, "error": None}
        except Exception as e:
            _jobs[job_id] = {"status": "error", "result": None, "error": str(e)}

    background_tasks.add_task(_run)
    return {"job_id": job_id, "status": "running"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    """Poll job status and result."""
    job = _jobs.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"error": "Job not found"})
    return job


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "MIRROR", "version": "1.0.0"}


@app.get("/stats")
def stats():
    """Return job statistics."""
    return {
        "total_jobs": len(_jobs),
        "running": sum(1 for j in _jobs.values() if j["status"] == "running"),
        "complete": sum(1 for j in _jobs.values() if j["status"] == "complete"),
        "error": sum(1 for j in _jobs.values() if j["status"] == "error"),
    }
