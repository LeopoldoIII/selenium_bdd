import os
from datetime import datetime


class ScreenshotManager:
    directory = "screenshots"

    @classmethod
    def initialize_directory(cls):
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

    @classmethod
    def take_screenshot(cls, driver, step_name):
        cls.initialize_directory()

        # Generate the timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Clean up the step name to use it in the filename
        step_name = step_name.replace(" ", "_")

        # Create the filename
        filename = f"{cls.directory}/{step_name}_{timestamp}.png"

        # Take the screenshot and save it
        driver.save_screenshot(filename)
        return filename