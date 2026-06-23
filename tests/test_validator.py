import pytest
from chatbot.validator import InputValidator

def test_valid_input():
    validator = InputValidator()
    is_valid, clean = validator.validate_and_sanitize("  Hello World  ")
    assert is_valid is True
    assert clean == "Hello World"

def test_empty_input():
    validator = InputValidator()
    is_valid, clean = validator.validate_and_sanitize("   ")
    assert is_valid is False
    assert clean == ""

def test_none_input():
    validator = InputValidator()
    is_valid, clean = validator.validate_and_sanitize(None)
    assert is_valid is False
    assert clean == ""
