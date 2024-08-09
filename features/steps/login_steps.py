from behave import given, when, then

from pages.login_page import LoginPage
from utils.config_reader import get_property


@given('I open the login page')
def step_open_login_page(context):
    context.driver.get(get_property('url'))
    # login_page = LoginPage(context.driver)
    # login_page.enter_username("your_username")
    # login_page.enter_password("your_password")
    # login_page.click_login()


@when('I enter valid username and password')
def step_enter_credentials(context):
    print("Test")


@when('I click login')
def step_click_login(context):
    print("Test")


@then('I should see the homepage')
def step_see_homepage(context):
    print("Test")
    # assert 'Welcome' in driver.page_source
