import os
import allure

from utils.driver_factory import DriverFactory
from utils.api_client import ApiClient
from utils.screenshot_manager import ScreenshotManager
from utils.logger import setup_logger, get_logger

logger = get_logger("environment")


def before_all(context):
    setup_logger()
    logger.info("==================================================")
    logger.info("   Starting Behave Test Suite Execution")
    logger.info("==================================================")
    ScreenshotManager.initialize_directory()


def before_scenario(context, scenario):
    # Combine feature tags and scenario tags
    all_tags = set(scenario.effective_tags) if hasattr(scenario, "effective_tags") else set(scenario.tags)
    if hasattr(scenario, "feature") and hasattr(scenario.feature, "tags"):
        all_tags.update(scenario.feature.tags)

    logger.info(f"--- Starting Scenario: '{scenario.name}' [Tags: {list(all_tags)}] ---")

    is_api = "api" in all_tags
    is_ui = "ui" in all_tags or not is_api

    if is_ui:
        try:
            context.driver = DriverFactory.get_driver(context)
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver for '{scenario.name}': {e}")
            raise

    if is_api:
        context.api_client = ApiClient(context=context)


def before_step(context, step):
    context.step_name = step.name
    logger.info(f"  Step: {step.step_type.upper()} {step.name}")


def after_step(context, step):
    if step.status == "failed":
        logger.error(f"  FAILED Step: {step.step_type.upper()} {step.name}")
        if hasattr(context, "driver") and context.driver:
            ScreenshotManager.take_screenshot(context.driver, f"FAILED_{step.name}")


def after_scenario(context, scenario):
    logger.info(f"--- Finished Scenario: '{scenario.name}' Status: {scenario.status} ---")

    # Capture failure screenshot and attach to Allure if not captured already
    if scenario.status == "failed" and hasattr(context, "driver") and context.driver:
        try:
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name=f"Scenario_Failure_{scenario.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.debug(f"Could not attach final failure screenshot: {e}")

    # Safely quit WebDriver if it was instantiated
    if hasattr(context, "driver") and context.driver:
        try:
            context.driver.quit()
        except Exception as e:
            logger.warning(f"Error while quitting driver: {e}")
        finally:
            context.driver = None
