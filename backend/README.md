# AgriMitra Backend Service

Target Stack: **Python + FastAPI + PostgreSQL + SQLAlchemy + Alembic + Pydantic**

## Architecture Design

The backend is designed as a **Modular Monolith** with the following internal layout planned for upcoming phases:

```
backend/
├── app/
│   ├── api/            # FastAPI router endpoints & request handling
│   ├── services/       # Use case orchestration & workflow logic
│   ├── domain/         # Core business logic & decision engines
│   ├── db/             # Repositories, SQLAlchemy models, & migrations
│   └── core/           # Configuration & security settings
```

## Current Status

- **Phase 0:** Directory reserved. No application business logic, endpoints, or DB models implemented yet.
