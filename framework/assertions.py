def assert_status_code(response, expected_status):
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, "
        f"but got {response.status_code}"
    )


def assert_json_response(response):
    content_type = response.headers.get("Content-Type", "")

    assert "application/json" in content_type, (
        f"Expected JSON response, but got: {content_type}"
    )


def assert_response_time(response, max_seconds=10):
    response_time = response.elapsed.total_seconds()

    assert response_time <= max_seconds, (
        f"Response took {response_time:.2f}s, "
        f"expected <= {max_seconds}s"
    )


def assert_field_exists(data, field):
    assert field in data, (
        f"Expected field '{field}' to exist in response"
    )


def assert_field_value(data, field, expected_value):
    assert field in data, (
        f"Expected field '{field}' to exist in response"
    )

    assert data[field] == expected_value, (
        f"Expected '{field}' to be '{expected_value}', "
        f"but got '{data[field]}'"
    )