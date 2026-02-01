"""
GitVideo - Generate videos from Git repositories using OpenAI Sora
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
import uuid
import os

from app.services.repo_service import RepoService
from app.services.video_service import VideoService
from app.models.schemas import (
    VideoGenerationRequest,
    VideoGenerationResponse,
    VideoStatus,
    VideoStatusResponse
)

app = FastAPI(
    title="GitVideo API",
    description="Generate videos from Git repositories using OpenAI Sora",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for job status (use Redis/DB in production)
video_jobs: dict[str, VideoStatusResponse] = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "GitVideo API"}


@app.post("/api/generate", response_model=VideoGenerationResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Start video generation for a GitHub repository.
    
    This endpoint:
    1. Ingests the repository content
    2. Creates a video script based on the repo
    3. Generates a video using OpenAI Sora
    """
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    video_jobs[job_id] = VideoStatusResponse(
        job_id=job_id,
        status=VideoStatus.PENDING,
        message="Video generation queued",
        progress=0
    )
    
    # Start background task for video generation
    background_tasks.add_task(
        process_video_generation,
        job_id=job_id,
        repo_url=str(request.repo_url),
        api_key=request.openai_api_key,
        video_style=request.video_style,
        duration=request.duration
    )
    
    return VideoGenerationResponse(
        job_id=job_id,
        message="Video generation started",
        status_url=f"/api/status/{job_id}"
    )


async def process_video_generation(
    job_id: str,
    repo_url: str,
    api_key: str,
    video_style: str,
    duration: int
):
    """Background task to process video generation"""
    try:
        # Update status: Ingesting repository
        video_jobs[job_id].status = VideoStatus.PROCESSING
        video_jobs[job_id].message = "Analyzing repository..."
        video_jobs[job_id].progress = 5
        
        # Step 1: Ingest the repository
        repo_service = RepoService()
        repo_data = await repo_service.ingest_repository(repo_url)
        
        video_jobs[job_id].message = "Repository analyzed successfully"
        video_jobs[job_id].progress = 15
        
        # Step 2: Generate video script using GPT-4
        video_jobs[job_id].message = "Creating video script with AI..."
        video_jobs[job_id].progress = 20
        
        video_service = VideoService(api_key)
        script = await video_service.generate_script(repo_data)
        
        video_jobs[job_id].message = "Video script created"
        video_jobs[job_id].progress = 25
        
        # Step 3: Generate video using Sora (this is the long step)
        video_jobs[job_id].message = "Starting video generation with Sora (this may take several minutes)..."
        video_jobs[job_id].progress = 30
        
        # Generate video with progress callback
        video_path = await video_service.generate_video_with_progress(
            script=script,
            style=video_style,
            duration=duration,
            progress_callback=lambda p, m: update_sora_progress(job_id, p, m),
            image_urls=repo_data.image_urls
        )
        
        # Update final status
        video_jobs[job_id].status = VideoStatus.COMPLETED
        video_jobs[job_id].message = "Video generated successfully!"
        video_jobs[job_id].progress = 100
        # Store the local path for serving, but return API URL to frontend
        video_jobs[job_id].video_path = video_path
        video_jobs[job_id].video_url = f"http://localhost:8000/api/video/{job_id}"
        
    except Exception as e:
        video_jobs[job_id].status = VideoStatus.FAILED
        video_jobs[job_id].message = f"Error: {str(e)}"
        video_jobs[job_id].progress = 0


def update_sora_progress(job_id: str, sora_progress: int, message: str):
    """Update progress based on Sora's progress (30-95% of total)"""
    if job_id in video_jobs:
        # Map Sora's 0-100% to our 30-95% range
        mapped_progress = 30 + int(sora_progress * 0.65)
        video_jobs[job_id].progress = min(mapped_progress, 95)
        video_jobs[job_id].message = message


@app.get("/api/status/{job_id}", response_model=VideoStatusResponse)
async def get_video_status(job_id: str):
    """Get the status of a video generation job"""
    if job_id not in video_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return video_jobs[job_id]


@app.get("/api/video/{job_id}")
async def get_video(job_id: str):
    """Download the generated video"""
    if job_id not in video_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = video_jobs[job_id]
    
    if job.status != VideoStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Video not ready yet")
    
    # Get video path (stored in video_path attribute)
    video_path = getattr(job, 'video_path', None) or job.video_url
    
    if not video_path:
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # If it's a local file path
    if os.path.exists(video_path):
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"gitvideo_{job_id}.mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Disposition": f"inline; filename=gitvideo_{job_id}.mp4"
            }
        )
    
    raise HTTPException(status_code=404, detail=f"Video file not found at {video_path}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
