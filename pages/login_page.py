from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = self.driver.find_element(By.ID, 'username')
        self.search_box = self.driver.find_element(By.XPATH, '//textarea[@class="gLFyf"]')
        self.password_field = self.driver.find_element(By.ID, 'password')
        self.login_button = self.driver.find_element(By.ID, 'login')

    def enter_username(self, username):
        self.username_field.send_keys(username)

    def enter_password(self, password):
        self.password_field.send_keys(password)

    def click_login(self):
        self.login_button.click()