from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = ""

    def login(self, username, password):
        self.open(self.url)
        self.send_keys_to_element(self.USERNAME_FIELD, username)
        self.send_keys_to_element(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)