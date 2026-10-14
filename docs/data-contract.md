# Data Contracts & Interface Specifications

This document defines the data contract standards and integration interfaces planned for AgriMitra.

---

## 1. Overview
Data contracts specify schema definitions, field validation rules, and structural expectations for data flowing between:
- Frontend and FastAPI API layer
- Domain Engines and Repositories
- Data ingestion pipelines and Soil Dataset Storage (`data/soil/`)
- External provider adapters (Weather, LLM, Embedding, Vector Store)

---

## 2. Soil Dataset Storage Specifications

### Raw Soil Data (`data/soil/raw/`)
* **Format Target:** CSV / GeoJSON / JSON files.
* **Access Rule:** Read-only by transformation scripts. Never modified directly in-place.
* **Expected Fields (Target):** Location / Coordinates, Soil Type, pH level, Nitrogen (N), Phosphorus (P), Potassium (K), Organic Matter, Moisture Content.

### Processed Soil Data (`data/soil/processed/`)
* **Format Target:** Normalized Parquet / Processed JSON.
* **Access Rule:** Generated via automated ingestion scripts in `scripts/`. Cleaned and validated against Pydantic schema contracts.

---

## 3. API Contract Guidelines

* All API request and response bodies MUST be specified using Pydantic schemas.
* API responses MUST use standard HTTP status codes and uniform JSON error structures.
* Breaking changes to API contracts require explicit ADR updates in `docs/decisions.md`.

---

## 4. External Provider Interfaces (Planned)

External service integrations will implement abstract base contracts:
* `WeatherProviderInterface`: `get_current_weather()`, `get_forecast()`
* `LLMProviderInterface`: `generate_recommendation()`, `parse_query()`
* `EmbeddingProviderInterface`: `embed_text()`, `embed_batch()`
* `VectorStoreInterface`: `query_similar()`, `upsert_vectors()`
