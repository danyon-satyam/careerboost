# ADR-001: Use FastAPI as the Web Framework

**Date:** 2026-06-03
**Status:** Accepted
**Author:** Satyam Mohapatra

---

## Context

We need a Python web framework to build a REST API that:

- Handles 100+ concurrent users
- Integrates with ML models (Transformers, spaCy, scikit-learn)
- Auto-generates OpenAPI/Swagger documentation
- Supports async operations for real-time interview features
- Has strong type safety for maintainability

Candidates considered: FastAPI, Flask, Django REST Framework

---

## Decision

We will use **FastAPI 0.111.0**.

---

## Reasons

| Criteria          | FastAPI        | Flask     | Django REST    |
| ----------------- | -------------- | --------- | -------------- |
| Async support     | ✅ Native      | ❌ Add-on | ❌ Limited     |
| Auto Swagger docs | ✅ Built-in    | ❌ Plugin | ❌ Plugin      |
| Type hints        | ✅ Pydantic v2 | ❌ Manual | ❌ Serializers |
| Performance       | ✅ Fastest     | 🟡 Medium | 🟡 Medium      |
| Learning curve    | 🟡 Medium      | ✅ Low    | ❌ High        |

- Native async/await handles concurrent interview sessions without blocking
- Pydantic v2 integration gives automatic request validation and serialization
- Swagger UI at `/docs` — no extra documentation effort needed
- Type hints throughout — easier to catch bugs early, mentor-friendly code review
- 2–3x faster than Flask in benchmarks (critical for 100+ concurrent users target)

---

## Consequences

- Team must learn async/await patterns (acceptable — standard Python now)
- Dependency injection via `Depends()` is unfamiliar at first but very powerful
- All request/response shapes must be defined as Pydantic models (good practice)
- Slightly more boilerplate than Flask for simple routes (acceptable tradeoff)
