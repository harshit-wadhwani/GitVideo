"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from enum import Enum


class VideoStyle(str, Enum):
    """Available video styles"""
    CINEMATIC = "cinematic"
    TECH = "tech"
    MINIMAL = "minimal"
    DYNAMIC = "dynamic"
    DOCUMENTARY = "documentary"


class VideoStatus(str, Enum):
    """Video generation status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoGenerationRequest(BaseModel):
    """Request model for video generation"""
    repo_url: HttpUrl = Field(
        ...,
        description="GitHub repository URL",
        examples=["https://github.com/octocat/Hello-World"]
    )
    openai_api_key: str = Field(
        ...,
        min_length=20,
        description="OpenAI API key for Sora access"
    )
    video_style: VideoStyle = Field(
        default=VideoStyle.TECH,
        description="Style of the generated video"
    )
    duration: int = Field(
        default=8,
        ge=4,
        le=12,
        description="Video duration in seconds (4, 8, or 12)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/facebook/react",
                "openai_api_key": "sk-...",
                "video_style": "tech",
                "duration": 8
            }
        }


class VideoGenerationResponse(BaseModel):
    """Response model for video generation request"""
    job_id: str
    message: str
    status_url: str


class VideoStatusResponse(BaseModel):
    """Response model for video status check"""
    job_id: str
    status: VideoStatus
    message: str
    progress: int = Field(ge=0, le=100)
    video_url: Optional[str] = None
    video_path: Optional[str] = None  # Local file path for serving
    thumbnail_url: Optional[str] = None


class RepoData(BaseModel):
    """Repository data after ingestion"""
    name: str
    description: Optional[str] = None
    language: Optional[str] = None
    languages: list[str] = []
    topics: list[str] = []
    stars: int = 0
    forks: int = 0
    file_tree: str = ""
    summary: str = ""
    key_files: list[str] = []
    readme_content: Optional[str] = None
    image_urls: list[str] = []  # URLs to images in the repo (png, jpg, jpeg)
