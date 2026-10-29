import json
from behave import when, then


@when('I send a GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    context.response = context.api_client.get(endpoint)


@when('I send a POST request to "{endpoint}" with payload')
def step_send_post_request(context, endpoint):
    payload = json.loads(context.text)
    context.response = context.api_client.post(endpoint, json=payload)


@then('the response status code should be {status_code:d}')
def step_verify_status_code(context, status_code):
    assert context.response.status_code == status_code, (
        f"Expected status code {status_code}, but got {context.response.status_code}. "
        f"Response body: {context.response.text}"
    )


@then('the response body should contain key "{key}"')
def step_verify_key_in_body(context, key):
    json_data = context.response.json()
    assert key in json_data, f"Key '{key}' not found in response body: {json_data}"


@then('the response body key "{key}" should equal {expected_val:d}')
def step_verify_int_key_value(context, key, expected_val):
    json_data = context.response.json()
    assert json_data.get(key) == expected_val, (
        f"Expected key '{key}' to be {expected_val}, but got {json_data.get(key)}"
    )


@then('the response body key "{key}" should equal "{expected_val}"')
def step_verify_str_key_value(context, key, expected_val):
    json_data = context.response.json()
    assert str(json_data.get(key)) == expected_val, (
        f"Expected key '{key}' to be '{expected_val}', but got '{json_data.get(key)}'"
    )

