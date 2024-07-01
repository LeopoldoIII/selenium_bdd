import subprocess

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utils.config_reader import get_property


def get_driver():
    config = get_property("headless")
    chromedriver_path = get_property('chromedriver_path')
    options = webdriver.ChromeOptions()
    if config:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    else:
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--ignore-certificate-errors')
        # Uncomment and set the path if Chrome is installed in a custom location
        # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # pip install urllib3==1.26.6
    driver_service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=driver_service, options=options)
    # Set implicit wait time
    implicit_wait_time = get_property('implicit_wait_time')  # Default to 10 seconds if not specified
    driver.implicitly_wait(implicit_wait_time)
    return driver
