from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver):
        super().__init__(driver)
        self.url_step_one = "checkout-step-one.html"
        self.url_step_two = "checkout-step-two.html"

    def fill_your_information(self, first_name, last_name, postal_code):
        self.send_keys_to_element(self.FIRST_NAME_FIELD, first_name)
        self.send_keys_to_element(self.LAST_NAME_FIELD, last_name)
        self.send_keys_to_element(self.POSTAL_CODE_FIELD, postal_code)
        self.click_element(self.CONTINUE_BUTTON)

    def get_total_price(self):
        total_text = self.get_text_from_element(self.TOTAL_PRICE)
        return total_text.replace("Total: ", "")

    def click_finish(self):
        self.click_element(self.FINISH_BUTTON)