# AgriMitra Database Setup & Management Guide

## 1. Target Database Stack
* **RDBMS**: PostgreSQL (>= 15.0)
* **Python ORM**: SQLAlchemy 2.0 (AsyncIO)
* **Async Driver**: `asyncpg` (`postgresql+asyncpg://...`)
* **Migrations**: Alembic

---

## 2. Option A: Docker Compose Setup (Recommended)

If Docker & Docker Desktop are installed on your workstation:

```bash
# Start PostgreSQL service container
docker-compose -f docker/docker-compose.yml up -d

# Verify container status
docker-compose -f docker/docker-compose.yml ps
```

Connection parameters for `.env`:
```env
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=agrimitra
POSTGRES_PASSWORD=postgres_password_change_me
POSTGRES_DB=agrimitra_db
DATABASE_URL=postgresql+asyncpg://agrimitra:postgres_password_change_me@localhost:5432/agrimitra_db
```

---

## 3. Option B: Native PostgreSQL Installation

If running PostgreSQL directly on Windows / Linux without Docker:

1. Download and install PostgreSQL from [postgresql.org/download](https://www.postgresql.org/download/).
2. Launch `psql` or pgAdmin as the `postgres` administrative user:
   ```sql
   CREATE USER agrimitra WITH PASSWORD 'postgres_password_change_me';
   CREATE DATABASE agrimitra_db OWNER agrimitra;
   GRANT ALL PRIVILEGES ON DATABASE agrimitra_db TO agrimitra;
   ```
3. Update `backend/.env` with your local connection string.

---

## 4. Alembic Migration Commands

Navigate to `backend/` directory:

```bash
# Set PYTHONPATH
export PYTHONPATH=.   # Linux/macOS
$env:PYTHONPATH="."   # Windows PowerShell

# Check migration history
alembic history

# Run migrations up to latest revision
alembic upgrade head

# Rollback latest migration step
alembic downgrade -1
```
