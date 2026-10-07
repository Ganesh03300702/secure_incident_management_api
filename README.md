# Secure Incident Management REST API & Automated Testing Platform

A Python FastAPI project designed as an entry-level software engineering project demonstrating REST API development, authentication, input validation, database operations, automated testing, logging, and CI test execution.

## Features

- RESTful CRUD APIs for incident management
- Token-based authentication for protected endpoints
- Input validation using Pydantic
- SQLite database persistence
- Filtering by incident priority and status
- Error handling for invalid/missing resources
- Automated positive and negative API tests with PyTest
- GitHub Actions workflow for automated test execution
- OpenAPI/Swagger documentation

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python -m app
```

Open: http://127.0.0.1:8000/docs

## Demo credentials

Username: `admin`
Password: `admin123`

This is a demonstration credential for a local portfolio project only.

## Run tests

```bash
pytest -q
```

## API examples

Login:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

Create an incident:
```json
{
  "title": "API outage",
  "description": "Production API is unavailable",
  "priority": "high",
  "reporter": "Ganesh"
}
```

## Engineering focus

The project emphasizes clean API structure, validation, automated testing, negative test cases, error handling, database reliability, and repeatable CI execution.
