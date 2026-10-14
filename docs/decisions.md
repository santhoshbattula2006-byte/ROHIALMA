# Architectural Decision Records (ADRs)

## ADR-001: Adoption of Modular Monolith Architecture
* **Status:** Accepted
* **Context:** The system requires decoupled domain boundaries (soil processing, weather advisory, recommendation engines) without the complexity of microservice operational overhead during early development.
* **Decision:** Build AgriMitra as a single application codebase divided strictly into modular domain boundaries (FastAPI -> Services -> Engines -> Repositories -> Postgres).
* **Consequences:** Clear boundary enforcement, shared single database instance initially, easy refactoring path.

---

## ADR-002: Backend Technology Stack
* **Status:** Accepted
* **Context:** The backend requires robust asynchronous handling, data validation, ORM mapping, and database migration capabilities in Python.
* **Decision:** Select Python + FastAPI + PostgreSQL + SQLAlchemy + Alembic + Pydantic.
* **Consequences:** High developer velocity, native data science / analytics integration in Python, strong type verification via Pydantic.

---

## ADR-003: Frontend Technology Stack
* **Status:** Accepted
* **Context:** The user interface requires a responsive, component-driven framework with static typing and utility-first styling.
* **Decision:** Select React + TypeScript + Tailwind CSS.
* **Consequences:** Type safety across API payload types, standardized styling, component reusability.

---

## ADR-004: Strict Functionality Verification Policy
* **Status:** Accepted
* **Context:** Avoid premature or false completion assertions without empirical proof.
* **Decision:** Never claim functionality is working unless it has been executed and verified in the environment.
* **Consequences:** All components must undergo explicit execution checks before phase completion sign-off.
