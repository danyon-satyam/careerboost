# ADR-002: Use PostgreSQL over MongoDB

**Date:** 2026-06-03
**Status:** Accepted
**Author:** Satyam Mohapatra

---

## Context

CareerBoost needs to store:

- User profiles with structured fields (skills as JSON, experience as float)
- Jobs with required skills arrays and salary ranges
- Interviews linked to specific users AND jobs (relational)
- Questions linked to interviews, answers linked to questions (nested relations)
- Typing sessions and job applications

The data has clear relationships between entities.

---

## Decision

We will use **PostgreSQL 15** with SQLAlchemy 2.0 ORM.

---

## Reasons

- All 7 tables have clear foreign key relationships — relational model fits perfectly
- JOIN queries for interview → questions → answers are straightforward in SQL
- PostgreSQL supports JSON columns (used for `skills` array) — best of both worlds
- ACID compliance ensures interview data is never partially saved
- Cloud SQL (GCP) provides managed PostgreSQL — zero ops overhead in production
- SQLAlchemy provides excellent Python ORM with Alembic migration support

## Why not MongoDB

- Our data is relational, not document-based
- Joins across users/interviews/questions would require application-level logic
- Schema flexibility is not needed — our data model is well-defined
- Harder to enforce referential integrity

---

## Consequences

- Must design schema carefully upfront (done — 7 tables with ERD)
- Alembic migrations required for schema changes (good practice)
- Slightly less flexible for ad-hoc data (acceptable — we know our schema)
