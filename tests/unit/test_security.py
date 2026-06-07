import pytest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


def test_hash_password_returns_string():
    hashed = hash_password("mypassword")
    assert isinstance(hashed, str)
    assert hashed != "mypassword"


def test_hash_password_is_different_each_time():
    """bcrypt generates a unique salt each time."""
    hash1 = hash_password("mypassword")
    hash2 = hash_password("mypassword")
    assert hash1 != hash2


def test_verify_password_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "42"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token_valid():
    token = create_access_token({"sub": "42"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "42"


def test_decode_access_token_invalid():
    payload = decode_access_token("this.is.not.a.valid.token")
    assert payload is None


def test_decode_access_token_tampered():
    token = create_access_token({"sub": "42"})
    tampered = token + "tampered"
    payload = decode_access_token(tampered)
    assert payload is None
