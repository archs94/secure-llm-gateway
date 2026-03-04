# 🔐 Secure LLM Gateway

A secure API wrapper around OpenAI LLMs built with FastAPI.

This project demonstrates how to design and implement a **production-style secure middleware layer** that protects an LLM from abuse, injection attacks, and unauthorized access.

---

# 🚀 Overview

The Secure LLM Gateway acts as a protective layer between clients and an LLM provider (OpenAI).

It enforces:

- Authentication via API keys
- Role-Based Access Control (RBAC)
- Input validation and prompt injection detection
- Rate limiting (token bucket)
- Structured logging
- Secure secret management
- Structured error handling
- Unit testing
- Threat modeling (STRIDE)

The goal is to demonstrate secure backend design principles for AI systems.

---

# 🛡️ Security Features

## ✅ Server-Side Role Derivation
Client-supplied roles are never trusted.  
Roles are derived from API keys on the server to prevent privilege escalation.

## ✅ Input Validation & Prompt Injection Detection
- Rejects empty prompts
- Detects common injection patterns
- Prevents attempts to override system instructions

## ✅ Rate Limiting (Token Bucket)
Prevents:
- Abuse
- DoS attempts
- OpenAI quota exhaustion

Rate limiting is enforced per API key or role.

## ✅ Structured Logging
Logs are JSON formatted and include:
- Masked API key
- User role
- Prompt length
- Request latency
- Timestamp

No secrets are logged.

## ✅ Project Structure
secure-llm-gateway/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── validators.py
│   ├── rate_limiter.py
│   ├── llm_client.py
│   └── logger.py
│
├── tests/
│   └── test_token_bucket.py
│
├── docs/
│   ├── DESIGN.md
│   ├── THREAT_MODEL_STRIDE.md
│   └── ABUSE_CASES.md
│
├── requirements.txt
├── .gitignore
└── README.md