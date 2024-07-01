class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def send_text(self, element, text):
        element.clear()
        element.send_keys(text)

    def click(self, element):
        element.click()

    def find_element(self, *locator):
        return self.driver.find_element(*locator)
