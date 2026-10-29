import json
import os
from behave import given, when, then, use_step_matcher

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import get_property
from utils.screenshot_manager import ScreenshotManager


def _load_test_data():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "test_data.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


@given('I open the SauceDemo login page')
def step_open_login_page(context):
    url = get_property("BASE_URL", context=context) or get_property("ui.url", context=context) or "https://www.saucedemo.com"
    context.driver.get(url)
    context.login_page = LoginPage(context.driver)


use_step_matcher("re")


@when(r'I enter valid credentials for "(?P<user_type>[^"]*)" user')
def step_enter_valid_credentials(context, user_type):
    test_data = _load_test_data()
    user_info = test_data.get("saucedemo", {}).get("users", {}).get(user_type, {})

    username = user_info.get("username") or get_property("STANDARD_USER", context=context) or "standard_user"
    password = user_info.get("password") or get_property("STANDARD_PASSWORD", context=context) or "secret_sauce"

    context.login_page.enter_username(username)
    context.login_page.enter_password(password)


use_step_matcher("parse")


@when('I enter credentials for locked out user')
def step_enter_locked_credentials(context):
    test_data = _load_test_data()
    locked_info = test_data.get("saucedemo", {}).get("users", {}).get("locked", {})

    username = locked_info.get("username") or get_property("LOCKED_USER", context=context) or "locked_out_user"
    password = locked_info.get("password") or get_property("STANDARD_PASSWORD", context=context) or "secret_sauce"

    context.login_page.enter_username(username)
    context.login_page.enter_password(password)


@when('I click the login button')
def step_click_login(context):
    context.login_page.click_login()


@then('I should be redirected to the inventory products page')
def step_verify_inventory_page(context):
    context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.is_loaded(), "Inventory page was not loaded properly!"
    assert context.inventory_page.get_title_text().lower() == "products", f"Expected title 'Products', got '{context.inventory_page.get_title_text()}'"


use_step_matcher("re")


@then(r'I should see the error message "(?P<expected_message>[^"]*)"')
def step_verify_error_message(context, expected_message):
    assert context.login_page.is_error_displayed(), "Error container is not displayed!"
    actual_message = context.login_page.get_error_message()
    assert expected_message in actual_message, f"Expected '{expected_message}' to be in '{actual_message}'"


use_step_matcher("parse")


@then('I take a screenshot of the current page')
def step_take_screenshot(context):
    ScreenshotManager.take_screenshot(context.driver, context.step_name)

