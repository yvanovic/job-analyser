from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Job Analyzer API",
    description="ML-powered job posting analysis system",
    version="0.1.0",
)


# Pydantic models for request/response validation
#  Week 1: Basic Job Posting Management
# --------------------------------------------
# Define models for job postings
# --------------------------------------------
# Job Posting Model
# --------------------------------------------
# Define Pydantic models for job postings
# --------------------------------------------
class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: str
    description: str = Field(..., min_length=10)
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    posted_date: Optional[datetime] = None
    url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Senior Python Developer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "description": "We are looking for an experienced Python developer...",
                "salary_min": 120000,
                "salary_max": 180000,
                "url": "https://example.com/job/123",
            }
        }


# Response model for job postings (includes ID and timestamps)
# --------------------------------------------
class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    posted_date: Optional[datetime]
    url: Optional[str]
    created_at: datetime


# In-memory storage for Week 1 (we'll replace with DB in Week 2)
jobs_db = []
job_id_counter = 1


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {"message": "Job Analyzer API", "version": "0.1.0", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate):
    """Create a new job posting"""
    global job_id_counter

    job_data = job.model_dump()  # Convert Pydantic model to dict
    job_data["id"] = job_id_counter
    job_data["created_at"] = datetime.now()

    if job_data.get("posted_date") is None:
        job_data["posted_date"] = datetime.now()

    jobs_db.append(job_data)
    job_id_counter += 1

    return job_data


@app.get("/jobs", response_model=List[JobResponse])
def get_jobs(skip: int = 0, limit: int = 10):
    """Get list of job postings with pagination"""
    return jobs_db[skip : skip + limit]


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    """Get a specific job posting by ID"""
    for job in jobs_db:
        if job["id"] == job_id:
            return job

    raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    """Delete a job posting"""
    global jobs_db

    for i, job in enumerate(jobs_db):
        if job["id"] == job_id:
            deleted_job = jobs_db.pop(i)
            return {"message": "Job deleted successfully", "job": deleted_job}

    raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")


@app.get("/jobs/search/")
def search_jobs(query: str, skip: int = 0, limit: int = 10):
    """Search job postings by title or company"""
    results = [
        job
        for job in jobs_db
        if query.lower() in job["title"].lower()
        or query.lower() in job["company"].lower()
    ]
    return results[skip : skip + limit]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
