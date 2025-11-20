"""
Job models
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Metadata
    total_items = Column(Integer, default=0)
    items_processed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    owner = relationship("User", back_populates="jobs")
    project = relationship("Project", back_populates="jobs")
    results = relationship("JobResult", back_populates="job", cascade="all, delete-orphan")
    sources = relationship("JobSource", back_populates="job", cascade="all, delete-orphan")


class JobResult(Base):
    __tablename__ = "job_results"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    data = Column(JSON, nullable=False)  # Datos extraídos estructurados
    source_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    job = relationship("Job", back_populates="results")


class JobSource(Base):
    __tablename__ = "job_sources"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    url = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, crawled, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    job = relationship("Job", back_populates="sources")

