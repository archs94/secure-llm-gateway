# app/exceptions.py

class LLMGatewayError(Exception):
    """Custom exception for LLM Gateway errors"""
    pass


class ValidationError(Exception):
    """Raised when user input is invalid"""
    pass
