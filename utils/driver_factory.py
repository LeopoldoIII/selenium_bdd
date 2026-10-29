import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService

from utils.config_reader import get_property
from utils.logger import get_logger

logger = get_logger("driver_factory")


class DriverFactory:
    @staticmethod
    def get_driver(context=None):
        browser = str(get_property("browser", context=context, default="chrome")).lower().strip()
        headless = get_property("headless", context=context, default=False)
        implicit_wait = get_property("implicit_wait_time", context=context, default=0)

        logger.info(f"Initializing WebDriver for browser='{browser}' (headless={headless})")

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-notifications")
            options.add_argument("--ignore-certificate-errors")
            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            driver = webdriver.Firefox(options=options)

        elif browser in ("edge", "msedge"):
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1920,1080")
            driver = webdriver.Edge(options=options)

        elif browser == "safari":
            # Safari does not support headless mode natively
            options = webdriver.SafariOptions()
            driver = webdriver.Safari(options=options)
            driver.set_window_size(1920, 1080)

        else:
            raise ValueError(f"Unsupported browser: '{browser}'. Choose from 'chrome', 'firefox', 'edge', 'safari'.")

        if implicit_wait and implicit_wait > 0:
            driver.implicitly_wait(implicit_wait)

        logger.info(f"WebDriver for '{browser}' initialized successfully.")
        return driver

