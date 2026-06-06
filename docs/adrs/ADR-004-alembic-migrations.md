# ADR-004: Use Alembic for Database Migrations

**Date:** 2026-06-03
**Status:** Accepted
**Author:** Satyam M	ohapatra

---

## Context

As CareerBoost evolves over 30 days, the database schema will change:

- Week 1: Initial 7 tables
- Week 2: Possible additions for ML scoring columns
- Week 3: Job matching score columns
- Week 4: Performance indexes added

We need a way to track and apply schema changes safely.

---

## Decision

We will use **Alembic 1.13.1** integrated with SQLAlchemy.

---

## Reasons

- Official SQLAlchemy migration tool — no integration friction
- Auto-generates migration scripts from model changes (`--autogenerate`)
- Version-controlled migrations — every schema change tracked in git
- Supports upgrade and downgrade — safe rollback if deployment fails
- Works with both SQLite (testing) and PostgreSQL (production)

---

## Consequences

- Every model change requires a new migration file (`alembic revision --autogenerate`)
- Migration files must be committed to git alongside the model change
- CI/CD pipeline runs `alembic upgrade head` before starting the server
