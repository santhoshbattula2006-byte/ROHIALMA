# AgriMitra System Architecture

## Architecture Pattern: Modular Monolith

AgriMitra is designed as a **Modular Monolith**. All core business capabilities reside within a single deployment unit divided into strict, decoupled domain modules. This ensures high cohesion within modules, low coupling between modules, and a simplified deployment model while preserving clear boundaries for potential future microservice extraction.

---

## Core Data & Execution Flow

Request and data flow within the system follows a unidirectional layered structure:

```
Frontend (React + TypeScript + Tailwind)
   │
   ▼
FastAPI API (HTTP/REST Entry Points & Request Validation)
   │
   ▼
Services (Use Case Orchestration & Workflow Control)
   │
   ▼
Domain / Engines (Core Business Logic, Rules, Calculations & Algorithms)
   │
   ▼
Repositories (Data Access Abstractions & Persistence Logic)
   │
   ▼
PostgreSQL Database (Relational Data Store via SQLAlchemy)
```

### Layer Responsibilities

1. **Frontend**: Interactive user interface built with React, TypeScript, and Tailwind CSS.
2. **FastAPI API Layer**: Accepts incoming HTTP requests, performs input validation via Pydantic models, handles authentication/authorization headers, and maps responses.
3. **Services Layer**: Coordinates application use cases, manages database transactions, and orchestrates calls to domain engines and external integrations.
4. **Domain / Engines Layer**: Pure business logic, decision algorithms, soil analysis logic, and recommendation rules. Isolated from direct database access or HTTP handling.
5. **Repositories Layer**: Data access layer defining CRUD operations and custom queries using SQLAlchemy ORM.
6. **PostgreSQL**: Relational database storing primary domain data.

---

## Planned External Integrations (To Be Implemented in Future Phases)

The architecture reserves designated interfaces for external integrations to be added in subsequent phases:

* **Weather Provider**: External weather API for real-time and forecast meteorological data.
* **LLM Provider**: Large Language Model API for natural language assistance and context-aware guidance.
* **Embedding Provider**: Vector embedding service for semantic document search and RAG indexing.
* **Vector Store**: Vector database for storing and querying embeddings.
* **File Storage**: Blob storage or local file system for raw dataset storage and uploaded media.

---

## Current Status

* **Phase 0:** Repository structure initialized. Architectural specifications documented.
* No application business logic, models, or API endpoints have been implemented yet.
