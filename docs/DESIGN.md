# 1. Overview

The Secure LLM Gateway is a **secure middleware API layer** around an LLM (like OpenAI).  
It enforces authentication, authorization, input validation, rate limiting, logging, and structured error handling.  

**Goals:**
- Protect the LLM from abuse (DoS, injection attacks)  
- Enforce role-based access control (RBAC)  
- Provide structured logs for auditing  
- Safely manage secrets (API keys, OpenAI credentials)

## 2. Components

- **FastAPI Gateway** (`main.py`)  
  Receives requests, parses JSON, formats responses, and routes requests to the appropriate modules.

- **Authentication** (`auth.py`)  
  Verifies API keys and derives the user role server-side to prevent spoofing.

- **Role-Based Access Control (RBAC)**  
  `authorize(role, action)` ensures users only perform actions allowed for their role.

- **Input Validation** (`validators.py`)  
  Checks for empty prompts and detects prompt injection to protect the LLM from malicious inputs.

- **Rate Limiting** (`rate_limiter.py`)  
  Implements both sliding window (for testing) and token bucket (production) rate limiting per API key or role.

- **Logging** (`logger.py`)  
  Structured JSON logging that masks API keys and includes metadata such as role, prompt length, and request latency.

- **LLM Client** (`llm_client.py`)  
  Handles calls to the OpenAI API, captures errors, and raises structured exceptions like `LLMGatewayError`.

- **Error Handling**  
  Custom exceptions (`ValidationError`, `LLMGatewayError`) to provide consistent structured error responses.

- **Environment Variable Secrets**  
  Stores `API_GATEWAY_KEY` and OpenAI API keys in `.env` files, loaded securely via `python-dotenv`.

## 3. Architecture Diagram (Mermaid)

```mermaid
flowchart TD
    Client[Client App<br/>(curl / frontend)] --> Gateway[FastAPI Gateway<br/>main.py]
    Gateway --> Auth[Auth & RBAC<br/>auth.py]
    Gateway --> Validator[Input Validator<br/>validators.py]
    Gateway --> RateLimiter[Rate Limiter<br/>rate_limiter.py]
    Auth --> LLMClient[LLM Client<br/>llm_client.py]
    Validator --> LLMClient
    RateLimiter --> LLMClient
    LLMClient --> OpenAI[OpenAI API / LLM]
```markdown
