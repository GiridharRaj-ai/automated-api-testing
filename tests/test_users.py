import json
import pytest
from pathlib import Path

from framework.config import Config
from framework.assertions import (
    assert_status_code,
    assert_json_response,
    assert_response_time,
    assert_field_exists,
)
from framework.schema_validator import validate_json_schema


BASE_DIR = Path(__file__).resolve().parent.parent

USER_DATA_FILE = BASE_DIR / "test_data" / "user_data.json"
USER_SCHEMA_FILE = BASE_DIR / "schemas" / "user_schema.json"


def load_user_data():
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)


class TestUserCRUD:

    @pytest.mark.smoke
    def test_get_users(self, api_client):
        response = api_client.get(
            f"{Config.BASE_URL}/users"
        )

        assert_status_code(response, 200)
        assert_json_response(response)
        assert_response_time(response)

        data = response.json()

        assert_field_exists(data, "users")
        assert isinstance(data["users"], list)
        assert len(data["users"]) > 0

        user = data["users"][0]

        validate_json_schema(
            user,
            USER_SCHEMA_FILE
        )

    @pytest.mark.smoke
    def test_get_single_user(self, api_client):
        response = api_client.get(
            f"{Config.BASE_URL}/users/1"
        )

        assert_status_code(response, 200)
        assert_json_response(response)
        assert_response_time(response)

        data = response.json()

        assert_field_exists(data, "id")
        assert_field_exists(data, "firstName")
        assert_field_exists(data, "lastName")
        assert_field_exists(data, "email")

        assert data["id"] == 1

        validate_json_schema(
            data,
            USER_SCHEMA_FILE
        )

    @pytest.mark.smoke
    def test_create_user(self, api_client):
        data = load_user_data()
        user_data = data["create_user"]

        response = api_client.post(
            f"{Config.BASE_URL}/users/add",
            json=user_data
        )

        assert_status_code(response, 201)
        assert_json_response(response)
        assert_response_time(response)

        response_data = response.json()

        assert_field_exists(response_data, "id")
        assert response_data["firstName"] == user_data["firstName"]
        assert response_data["lastName"] == user_data["lastName"]
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]

    @pytest.mark.regression
    def test_update_user(self, api_client):
        data = load_user_data()
        updated_data = data["update_user"]

        response = api_client.put(
            f"{Config.BASE_URL}/users/1",
            json=updated_data
        )

        assert_status_code(response, 200)
        assert_json_response(response)
        assert_response_time(response)

        response_data = response.json()

        assert_field_exists(response_data, "firstName")
        assert_field_exists(response_data, "lastName")
        assert_field_exists(response_data, "email")

        assert response_data["firstName"] == updated_data["firstName"]
        assert response_data["lastName"] == updated_data["lastName"]
        assert response_data["email"] == updated_data["email"]

    @pytest.mark.regression
    def test_delete_user(self, api_client):
        response = api_client.delete(
            f"{Config.BASE_URL}/users/1"
        )

        assert_status_code(response, 200)
        assert_json_response(response)
        assert_response_time(response)

        response_data = response.json()

        assert_field_exists(response_data, "id")
        assert_field_exists(response_data, "isDeleted")

        assert response_data["id"] == 1
        assert response_data["isDeleted"] is True

    @pytest.mark.regression
    def test_search_users(self, api_client):
        response = api_client.get(
            f"{Config.BASE_URL}/users/search",
            params={"q": "John"}
        )

        assert_status_code(response, 200)
        assert_json_response(response)
        assert_response_time(response)

        data = response.json()

        assert_field_exists(data, "users")
        assert isinstance(data["users"], list)


class TestUserNegative:

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "endpoint, expected_status",
        [
            ("/users/9999", 404),
            ("/invalid-endpoint", 404),
            ("/users/abc", 400),
        ]
    )
    def test_invalid_get_requests(
        self,
        api_client,
        endpoint,
        expected_status
    ):
        response = api_client.get(
            f"{Config.BASE_URL}{endpoint}"
        )

        assert_status_code(
            response,
            expected_status
        )

        assert_response_time(response)