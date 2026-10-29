import os
from datetime import datetime
import allure

from utils.logger import get_logger

logger = get_logger("screenshot_manager")


class ScreenshotManager:
    directory = "screenshots"

    @classmethod
    def initialize_directory(cls):
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory, exist_ok=True)

    @classmethod
    def take_screenshot(cls, driver, step_name):
        cls.initialize_directory()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_step_name = step_name.replace(" ", "_").replace("/", "_").replace('"', "")
        filename = f"{cls.directory}/{clean_step_name}_{timestamp}.png"

        try:
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved to {filename}")

            # Attach to Allure Report
            with open(filename, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=step_name,
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            logger.error(f"Failed to capture screenshot for '{step_name}': {e}")

        return filename
