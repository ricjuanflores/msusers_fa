# Users Microservice FA

## Tech Stack

- FastAPI
- PostgreSQL
- Redis
- Celery
- SQLAlchemy
- Alembic
- Docker
- Kubernetes
- Github Actions

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Routers (API Layer)                  │
│              HTTP endpoints, request validation         │
├─────────────────────────────────────────────────────────┤
│                   Services (Business Logic)             │
│            Domain logic, orchestration, validation      │
├─────────────────────────────────────────────────────────┤
│                 Repositories (Data Access)              │
│              Database queries, caching strategies       │
├─────────────────────────────────────────────────────────┤
│                    Models (Domain Layer)                │
│              SQLAlchemy models, Pydantic schemas        │
└─────────────────────────────────────────────────────────┘
```

## Requirements

- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose

## Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone git@github.com:ricjuanflores/msusers_fa.git
cd msusers_fa

# Copy environment configuration
cp .env.example .env

# Build and start all services
docker-compose up -d --build

# Verify services are running
docker-compose ps
```

### Local Development Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Configure environment variables
cp .env.example .env
# Edit .env with your local configuration

# Run database migrations
alembic upgrade head

# Start development server with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Environment Variables

Create a `.env` file in the project root

## Project Structure

```
msusers_fa/
├── main.py                     # Application entry point
├── ms_fa/
│   ├── __init__.py             # FastAPI app factory
│   ├── config/                 # Configuration management
│   ├── db/                     # Database and cache connections
│   ├── helpers/                # Utilities (JWT, hashing, notifications)
│   ├── middlewares/            # Authentication and custom middlewares
│   ├── models/                 # SQLAlchemy ORM models
│   ├── repositories/           # Data access layer (Repository pattern)
│   ├── routers/                # API route definitions
│   ├── schemas/                # Pydantic request/response schemas
│   ├── services/               # Business logic layer
│   └── tasks/                  # Celery async tasks
├── migrations/                 # Alembic database migrations
├── k8s/                        # Kubernetes manifests (staging & prod)
├── docker/                     # Docker configuration files
│   ├── ms-cron                 # Cron job definitions
│   └── redis.conf              # Redis configuration
├── .github/workflows/          # CI/CD pipeline definitions
├── docker-compose.yml          # Local development orchestration
├── Dockerfile                  # Multi-environment container build
├── start.sh                    # Entrypoint script (handles env-based startup)
└── requirements.txt            # Python dependencies
```

### Database Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration (auto-generate from model changes)
alembic revision --autogenerate -m "add_user_preferences_table"

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

### Testing

```bash
# Run test suite
pytest

# Run with coverage report
pytest --cov=ms_fa --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Celery Workers

```bash
# Start Celery worker
celery -A ms_fa.tasks.worker worker --loglevel=info

# Start Celery beat (scheduler)
celery -A ms_fa.tasks.worker beat --loglevel=info

# Monitor tasks with Flower (optional)
celery -A ms_fa.tasks.worker flower
```

### Kubernetes

Kubernetes manifests are located in the `k8s/` directory:

- `stg_manifest.yml` - Staging API deployment
- `stg_manifest_celery.yml` - Staging Celery worker
- `prod_manifest.yml` - Production API deployment
- `prod_manifest_celery.yml` - Production Celery worker
