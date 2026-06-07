# ADR-005: Use Browser Web Speech API for Speech-to-Text

**Date:** 2026-06-07
**Status:** Accepted
**Author:** Danyon Satyam

---

## Context

CareerBoost AI interview requires candidates to **speak** their answers —
not type. We need to convert spoken audio to text before passing to the
AI evaluation pipeline.

Options considered:

- OpenAI Whisper (local model)
- Google Cloud Speech-to-Text (paid)
- AWS Transcribe (paid)
- **Browser Web Speech API (free, built-in)**

---

## Decision

Use the **browser's built-in Web Speech API** (`SpeechRecognition`)
for real-time speech-to-text on the frontend.

The transcript text is sent to FastAPI as a string — the backend
never handles raw audio files.

---

## Reasons

- Completely free — zero API calls, zero cost
- Real-time — transcript appears as candidate speaks
- No backend audio processing — reduces server load significantly
- Chrome support is excellent (used by 65%+ of users)
- Transcript quality is good enough for technical interview answers
- Simplest possible architecture — text in, text out

## Flow

Candidate speaks into microphone
↓
Browser Web Speech API (SpeechRecognition)
↓
Real-time transcript text (shown on screen)
↓
Frontend sends transcript text to FastAPI
↓
Gemini + spaCy evaluation pipeline
↓
Score + feedback returned

---



## Consequences

- Only works in Chrome/Edge (Firefox doesn't support Web Speech API)
- Requires HTTPS in production (localhost works fine for dev)
- No audio recording stored — privacy friendly
- Candidate sees their transcript live — good UX
- Fallback: if speech fails, candidate can type (graceful degradation)
