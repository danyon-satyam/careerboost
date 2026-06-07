import pytest


class TestSignup:
    def test_signup_success(self, client, sample_user_data):
        response = client.post(
            "/api/v1/auth/signup",
            json=sample_user_data
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert "id" in data
        assert "password_hash" not in data  # never expose hash

    def test_signup_duplicate_email(self, client, sample_user_data):
        client.post("/api/v1/auth/signup", json=sample_user_data)
        response = client.post(
            "/api/v1/auth/signup",
            json=sample_user_data
        )
        assert response.status_code == 409

    def test_signup_invalid_email(self, client):
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "not-an-email",
                "password": "pass123",
                "full_name": "Test"
            }
        )
        assert response.status_code == 422

    def test_signup_missing_fields(self, client):
        response = client.post(
            "/api/v1/auth/signup",
            json={"email": "test@test.com"}
        )
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, sample_user_data, registered_user):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(
        self, client, sample_user_data, registered_user
    ):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nobody@nowhere.com",
                "password": "pass123"
            }
        )
        assert response.status_code == 401

    def test_login_returns_valid_jwt(
        self, client, sample_user_data, registered_user
    ):
        from app.core.security import decode_access_token
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )
        token = response.json()["access_token"]
        payload = decode_access_token(token)
        assert payload is not None
        assert "sub" in payload


class TestUserProfile:
    def test_get_profile_authenticated(
        self, client, registered_user, auth_headers
    ):
        response = client.get(
            "/api/v1/users/profile",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == registered_user["email"]

    def test_get_profile_unauthenticated(self, client):
        response = client.get("/api/v1/users/profile")
        assert response.status_code == 403

    def test_get_profile_invalid_token(self, client):
        response = client.get(
            "/api/v1/users/profile",
            headers={"Authorization": "Bearer fake.token.here"}
        )
        assert response.status_code == 401

    def test_update_profile_success(
        self, client, registered_user, auth_headers
    ):
        response = client.patch(
            "/api/v1/users/profile",
            json={
                "full_name": "Updated Name",
                "target_role": "Senior Engineer",
                "experience_years": 3.5
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["target_role"] == "Senior Engineer"
        assert data["experience_years"] == 3.5

    def test_update_profile_unauthenticated(self, client):
        response = client.patch(
            "/api/v1/users/profile",
            json={"full_name": "Hacker"}
        )
        assert response.status_code == 403
