# AI Analyst Agent For Agriculture Analytics and Prediction 

AI Analyst Agent For Agriculture Analytics and Prediction 
is an AI-powered agricultural advisory platform designed as a modular monolith.

> **CRITICAL RULE**
> Never claim functionality is working unless it has been executed and verified.

---

## Repository Structure

```
.
├── backend/                # Python + FastAPI backend service (Modular Monolith)
├── frontend/               # React + TypeScript + Tailwind frontend application
├── data/
│   └── soil/
│       ├── raw/           # Raw soil dataset storage
│       └── processed/     # Processed soil datasets
├── scripts/                # Utility and administration scripts
├── docs/                   # Architectural documentation & specifications
│   ├── architecture.md
│   ├── phases.md
│   ├── decisions.md
│   └── data-contract.md
└── docker/                 # Containerization configs & docker-compose setups
```

---

## Target Technology Stack

* **Backend:** Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic
* **Frontend:** React, TypeScript, Tailwind CSS
* **Architecture:** Modular Monolith

---

## Getting Started

1. Copy `.env.example` to `.env` and configure local variables.
2. Refer to `docs/architecture.md` for architectural design and layer responsibilities.
3. Refer to `docs/phases.md` for project roadmap and execution phases.
