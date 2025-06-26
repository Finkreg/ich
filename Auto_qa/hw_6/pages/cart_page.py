from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "cart.html"

    def click_checkout(self):
        self.click_element(self.CHECKOUT_BUTTON)