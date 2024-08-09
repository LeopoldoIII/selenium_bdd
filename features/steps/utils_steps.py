from behave import given, when, then

from utils.screenshot_manager import ScreenshotManager


@then("Take a picture of the current page")
def take_a_picture_of_the_current_page(context):
    ScreenshotManager.take_screenshot(context.driver, context.step_name)
