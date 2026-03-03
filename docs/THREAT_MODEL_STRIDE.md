# STRIDE Threat Model — Secure LLM Gateway

This document describes potential security threats for the Secure LLM Gateway using the STRIDE framework.  
It includes examples, likelihood, impact, and mitigations for each category.

---

## **S – Spoofing**

**Threat:** An attacker uses a stolen API key to impersonate a legitimate user.  
**Example:** Sending `/generate` requests with someone else’s `x-api-key`.  
**Likelihood:** Medium  
**Impact:** High — unauthorized access, quota abuse, and potential cost increase.  

**Mitigation:**
- Require strong, randomly generated API keys.
- Store secrets securely in environment variables.
- Rotate API keys periodically.
- Log all API key usage for auditing.

---

## **T – Tampering**

**Threat:** Modifying requests to inject malicious prompts or bypass validation.  
**Example:** `{"prompt": "DROP TABLE users;"}` or attempts to escape validation.  
**Likelihood:** Medium  
**Impact:** Medium — LLM could reveal sensitive info or downstream abuse may occur.  

**Mitigation:**
- Validate all input via `validate_prompt`.
- Reject known injection patterns.
- Escape sensitive content before passing to LLM.
- Add unit tests covering injection attempts.

---

## **R – Repudiation**

**Threat:** Users deny sending malicious or unwanted requests.  
**Example:** A user claims they didn’t send spammy or abusive requests.  
**Likelihood:** Low  
**Impact:** Medium — could complicate auditing or investigation.  

**Mitigation:**
- Structured JSON logging via `log_event`.
- Include timestamp, role, masked API key, prompt length, and latency.
- Maintain logs for auditing.

---

## **I – Information Disclosure**

**Threat:** Sensitive data could be leaked through logs or LLM responses.  
**Example:** API keys logged in plaintext, or prompts contain secrets revealed by the LLM.  
**Likelihood:** Medium  
**Impact:** High — sensitive user data or credentials could be exposed.  

**Mitigation:**
- Mask API keys in logs (e.g., `supe***key`).
- Avoid logging the full prompt content in production.
- Keep secrets in environment variables, not in code.

---

## **D – Denial of Service (DoS)**

**Threat:** Excessive requests consume resources or exhaust OpenAI quota.  
**Example:** A user floods the API causing others to get `429 Too Many Requests`.  
**Likelihood:** High  
**Impact:** High — service disruption and potential cost increases.  

**Mitigation:**
- Token bucket rate limiting per role or per API key.
- Sliding window limiter for testing and comparison.
- Monitor usage and set alerts for abnormal spikes.

---

## **E – Elevation of Privilege**

**Threat:** A user bypasses RBAC to perform actions they shouldn’t.  
**Example:** A regular user executes admin commands or accesses privileged data.  
**Likelihood:** Low  
**Impact:** High — data or control could be compromised.  

**Mitigation:**
- Enforce `authorize(role, action)` on every endpoint.
- Never trust client-supplied `role` directly; derive role from API key.
- Write unit tests to cover all RBAC rules.

---

**Notes:**

- Logging, RBAC, rate limiting, and input validation work together to mitigate multiple STRIDE threats.  
- Future improvements could include per-API-key limits, alerting dashboards, and stricter secret handling.
