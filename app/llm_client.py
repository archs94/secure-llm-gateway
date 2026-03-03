import os

USE_MOCK = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

if not USE_MOCK:
    from openai import OpenAI
    from app.exceptions import LLMGatewayError

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def query_llm(prompt: str, model: str = "gpt-3.5-turbo"):
    if USE_MOCK:
        # Mock response for development/testing
        return f"[MOCK RESPONSE] Echo: {prompt}"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise LLMGatewayError(f"LLM request failed: {str(e)}")
