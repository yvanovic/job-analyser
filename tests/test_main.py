from fastapi.testclient import TestClient
from app.main import app, jobs_db, job_id_counter
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the in-memory database before each test"""
    jobs_db.clear()
    # Reset counter (note: this is a simplification for Week 1)
    yield
    jobs_db.clear()


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["version"] == "0.1.0"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()


def test_create_job():
    """Test creating a job posting"""
    job_data = {
        "title": "Python Developer",
        "company": "Test Corp",
        "location": "Remote",
        "description": "Looking for a talented Python developer with 3+ years experience",
        "salary_min": 100000,
        "salary_max": 150000,
    }

    response = client.post("/jobs", json=job_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == job_data["title"]
    assert data["company"] == job_data["company"]
    assert "id" in data
    assert "created_at" in data
    assert "posted_date" in data


def test_create_job_validation():
    """Test job creation with invalid data"""
    # Missing required fields
    invalid_job = {"title": "Dev", "company": "Test"}

    response = client.post("/jobs", json=invalid_job)
    assert response.status_code == 422  # Validation error


def test_get_jobs_empty():
    """Test getting jobs when database is empty"""
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.json() == []


def test_get_jobs():
    """Test getting list of jobs"""
    # Create some jobs first
    job1 = {
        "title": "Backend Engineer",
        "company": "Company A",
        "location": "NYC",
        "description": "Backend position at Company A",
    }
    job2 = {
        "title": "Frontend Engineer",
        "company": "Company B",
        "location": "SF",
        "description": "Frontend position at Company B",
    }

    client.post("/jobs", json=job1)
    client.post("/jobs", json=job2)

    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_jobs_pagination():
    """Test job listing pagination"""
    # Create 5 jobs
    for i in range(5):
        job = {
            "title": f"Developer {i}",
            "company": f"Company {i}",
            "location": "Remote",
            "description": f"Job description {i}",
        }
        client.post("/jobs", json=job)

    # Get first 2
    response = client.get("/jobs?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Get next 2
    response = client.get("/jobs?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_job_by_id():
    """Test getting a specific job"""
    job_data = {
        "title": "Data Scientist",
        "company": "ML Corp",
        "location": "Boston",
        "description": "Data science position",
    }

    create_response = client.post("/jobs", json=job_data)
    job_id = create_response.json()["id"]

    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["title"] == job_data["title"]


def test_get_nonexistent_job():
    """Test getting a job that doesn't exist"""
    response = client.get("/jobs/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_job():
    """Test deleting a job"""
    job_data = {
        "title": "DevOps Engineer",
        "company": "Cloud Inc",
        "location": "Seattle",
        "description": "DevOps position",
    }

    create_response = client.post("/jobs", json=job_data)
    job_id = create_response.json()["id"]

    # Delete the job
    delete_response = client.delete(f"/jobs/{job_id}")
    assert delete_response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/jobs/{job_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_job():
    """Test deleting a job that doesn't exist"""
    response = client.delete("/jobs/9999")
    assert response.status_code == 404
