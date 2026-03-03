import re
from app.exceptions import ValidationError

# Patterns that indicate dangerous input
FORBIDDEN_PATTERNS = [
    r"rm -rf",         # dangerous shell command
    r"sudo",           # privilege escalation
    r"DROP TABLE",     # SQL injection
    r"<script>",       # XSS
    r"\\x[0-9a-fA-F]{2}"  # hex injection
]


def validate_prompt(prompt: str):
    """
    Validates user prompt to prevent injection and empty input.
    Raises ValidationError if invalid.
    """
    if not prompt or not prompt.strip():
        raise ValidationError("Prompt cannot be empty")

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            raise ValidationError(f"Potential injection detected: {pattern}")
