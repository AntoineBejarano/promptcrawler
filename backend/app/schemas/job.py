"""
Job schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.models.job import JobStatus


class JobBase(BaseModel):
    prompt: str
    project_id: Optional[int] = None


class JobCreate(JobBase):
    pass


class JobResult(BaseModel):
    id: int
    job_id: int
    data: Dict[str, Any]
    source_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    id: int
    prompt: str
    status: JobStatus
    owner_id: int
    project_id: Optional[int] = None
    total_items: int
    items_processed: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    results: List[JobResult] = []

    class Config:
        from_attributes = True


class Job(JobResponse):
    pass


class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int

