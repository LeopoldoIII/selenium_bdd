from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("login_page")


class LoginPage(BasePage):
    # SauceDemo Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_username(self, username):
        logger.info(f"Entering username: '{username}'")
        self.send_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        logger.info("Entering password: '***'")
        self.send_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_CONTAINER)
