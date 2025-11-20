"""
Jobs endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.job import Job, JobStatus, JobResult, JobSource
from app.schemas.job import JobCreate, JobResponse, JobListResponse
from app.services.perplexity import PerplexityService
from app.services.crawler import CrawlerService
from app.services.extractor import ExtractorService
from app.workers.job_worker import process_job
from rq import Queue
from redis import Redis
from app.config import settings
import json

router = APIRouter()

# Redis queue
redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue("default", connection=redis_conn)


@router.post("", response_model=JobResponse, status_code=201)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo job"""
    # Verificar límites según plan
    if current_user.plan == "free" and current_user.jobs_count >= 5:
        raise HTTPException(
            status_code=403,
            detail="Free plan limit reached (5 jobs/month)"
        )
    
    # Crear job
    db_job = Job(
        prompt=job_data.prompt,
        owner_id=current_user.id,
        project_id=job_data.project_id,
        status=JobStatus.PENDING
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Encolar job para procesamiento
    queue.enqueue(process_job, db_job.id)
    
    return db_job


@router.get("", response_model=JobListResponse)
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar jobs del usuario"""
    jobs = db.query(Job).filter(Job.owner_id == current_user.id)\
        .order_by(Job.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    total = db.query(Job).filter(Job.owner_id == current_user.id).count()
    
    return JobListResponse(jobs=jobs, total=total)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener detalles de un job"""
    job = db.query(Job).filter(Job.id == job_id, Job.owner_id == current_user.id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.get("/{job_id}/results")
async def get_job_results(
    job_id: int,
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener resultados de un job en JSON o CSV"""
    job = db.query(Job).filter(Job.id == job_id, Job.owner_id == current_user.id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    results = db.query(JobResult).filter(JobResult.job_id == job_id).all()
    
    if format == "json":
        return {
            "job_id": job_id,
            "results": [{"id": r.id, "data": r.data, "source_url": r.source_url} for r in results]
        }
    else:  # CSV
        import csv
        from io import StringIO
        
        output = StringIO()
        if results and results[0].data:
            # Obtener todas las keys únicas
            all_keys = set()
            for r in results:
                if isinstance(r.data, dict):
                    all_keys.update(r.data.keys())
            
            writer = csv.DictWriter(output, fieldnames=list(all_keys) + ["source_url"])
            writer.writeheader()
            for r in results:
                row = r.data.copy() if isinstance(r.data, dict) else {}
                row["source_url"] = r.source_url
                writer.writerow(row)
        
        return {"csv": output.getvalue()}

