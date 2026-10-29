from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.config_reader import get_property
from utils.logger import get_logger

logger = get_logger("base_page")


class BasePage:
    def __init__(self, driver, timeout=None):
        self.driver = driver
        timeout_val = timeout or get_property("EXPLICIT_TIMEOUT") or get_property("explicit_timeout") or 10
        self.timeout = int(timeout_val)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator):
        """Wait until element is present in DOM and visible."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for visibility of element with locator: {locator}")
            raise

    def find_elements(self, locator):
        """Wait until at least one element is present in DOM."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for elements with locator: {locator}")
            raise

    def click(self, locator):
        """Wait until element is clickable and click it."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.debug(f"Clicked element: {locator}")
        except TimeoutException:
            logger.error(f"Timeout waiting for element to be clickable: {locator}")
            raise

    def send_text(self, locator, text):
        """Wait until element is visible, clear it, and type text."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.debug(f"Typed '{text}' into element: {locator}")

    def get_text(self, locator):
        """Wait until element is visible and return text."""
        element = self.find_element(locator)
        text = element.text
        logger.debug(f"Read text '{text}' from element: {locator}")
        return text

    def is_visible(self, locator, timeout=3):
        """Check if an element is visible within a short timeout without throwing."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title
