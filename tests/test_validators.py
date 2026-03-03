from app.validators import validate_prompt
from app.exceptions import ValidationError


def test_valid_prompt():
    validate_prompt("Hello world")
    print("Valid prompt passed ✅")


def test_empty_prompt():
    try:
        validate_prompt("")
    except ValidationError as e:
        print("Empty prompt caught ✅", e)


def test_injection_prompt():
    try:
        validate_prompt("DROP TABLE users")
    except ValidationError as e:
        print("Injection prompt caught ✅", e)


# Run all tests
test_valid_prompt()
test_empty_prompt()
test_injection_prompt()
