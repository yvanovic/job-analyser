![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![Status](https://img.shields.io/badge/status-week%201%20complete-success)

# Job Analyzer API - Week 1

ML-powered job posting analysis system for learning backend, ML engineering, and automation.

## Week 1 Goals

✅ Setup FastAPI project structure
✅ Create basic CRUD endpoints for job postings
✅ Implement request/response validation with Pydantic
✅ Write unit tests with pytest

## Project Structure

```
job-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with endpoints
│   ├── api/                 # Future: route handlers
│   ├── models/              # Future: database models
│   └── services/            # Future: business logic
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Unit tests
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Create Project Directory

```bash
mkdir job-analyzer
cd job-analyzer
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Directory Structure

```bash
mkdir -p app/{api,models,services} tests
touch app/__init__.py app/api/__init__.py tests/__init__.py
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### 6. View Interactive API Docs

Open your browser to: `http://localhost:8000/docs`

FastAPI automatically generates interactive Swagger documentation!

### 7. Run Tests

```bash
pytest tests/ -v
```

## API Endpoints

### `GET /`

Root endpoint with API information

### `GET /health`

Health check endpoint

### `POST /jobs`

Create a new job posting

**Request body:**

```json
{
  "title": "Senior Python Developer",
  "company": "Tech Corp",
  "location": "San Francisco, CA",
  "description": "We are looking for an experienced Python developer...",
  "salary_min": 120000,
  "salary_max": 180000,
  "url": "https://example.com/job/123"
}
```

### `GET /jobs`

Get list of all jobs (with pagination)

**Query parameters:**

- `skip`: Number of jobs to skip (default: 0)
- `limit`: Maximum number of jobs to return (default: 10)

### `GET /jobs/{job_id}`

Get a specific job by ID

### `DELETE /jobs/{job_id}`

Delete a job posting

## Testing the API

### Using curl

```bash
# Create a job
curl -X POST "http://localhost:8000/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Developer",
    "company": "Test Corp",
    "location": "Remote",
    "description": "Great opportunity for Python developers"
  }'

# Get all jobs
curl "http://localhost:8000/jobs"

# Get specific job
curl "http://localhost:8000/jobs/1"
```

### Using the interactive docs

1. Go to `http://localhost:8000/docs`
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

## Week 1 Accomplishments

- ✅ FastAPI server running
- ✅ CRUD operations for jobs
- ✅ Pydantic validation
- ✅ In-memory storage (temporary)
- ✅ Comprehensive test suite
- ✅ Auto-generated API documentation

## Next Week (Week 2)

- Add PostgreSQL database
- Replace in-memory storage with real persistence
- Add SQLAlchemy ORM
- Implement database migrations with Alembic
- Learn about database connections and sessions

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

---
