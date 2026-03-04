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

## 📂 Project Structure

The project follows a layered, security-first architecture with clear separation of concerns.

```text
secure-llm-gateway/
│
├── app/                             # Application Layer
│   ├── main.py                      # FastAPI entry point & route definitions
│   ├── auth.py                      # Authentication & RBAC enforcement
│   ├── validators.py                # Input validation & prompt injection detection
│   ├── rate_limiter.py              # Token bucket rate limiting
│   ├── llm_client.py                # OpenAI API wrapper
│   └── logger.py                    # Structured logging utilities
│
├── tests/                           # Test Layer
│   └── test_token_bucket.py         # Unit tests
│
├── docs/                            # Documentation Layer
│   ├── DESIGN.md                    # Architecture & system design
│   ├── THREAT_MODEL_STRIDE.md       # STRIDE threat model
│   └── ABUSE_CASES.md               # Abuse case analysis
│
├── requirements.txt                 # Project dependencies
├── .gitignore                       # Ignored files and secrets
└── README.md                        # Project overview