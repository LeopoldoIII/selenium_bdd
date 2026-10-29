from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("inventory_page")


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        super().__init__(driver)

    def is_loaded(self):
        return self.is_visible(self.TITLE) and "inventory.html" in self.get_current_url()

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_item_count(self):
        items = self.find_elements(self.INVENTORY_ITEMS)
        return len(items)

