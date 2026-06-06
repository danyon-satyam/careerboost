# ADR-003: Use JWT for Stateless Authentication

**Date:** 2026-06-03
**Status:** Accepted
**Author:** Satyam Mohapatra

---

## Context

CareerBoost needs authentication for:

- Recruiters creating and managing interview agents
- Candidates taking interviews (short-lived sessions)
- Protected API endpoints (profile, analytics, job applications)

Options: JWT (stateless), Session-based (stateful), OAuth2 only

---

## Decision

We will use **JWT (JSON Web Tokens)** with python-jose and bcrypt password hashing.

---

## Reasons

- Stateless — no server-side session storage needed, scales horizontally on Cloud Run
- Self-contained — token carries user ID, no DB lookup on every request
- Standard — works seamlessly with FastAPI's `OAuth2PasswordBearer`
- Short-lived access tokens (30 min) + refresh token pattern for security
- bcrypt for password hashing — industry standard, built-in salt

---

## Consequences

- Tokens cannot be invalidated before expiry (acceptable — short TTL mitigates this)
- Token size larger than session cookie (acceptable — small payload)
- Must implement refresh token endpoint for good UX
