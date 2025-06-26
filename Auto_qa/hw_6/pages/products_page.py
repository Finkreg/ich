from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductsPage(BasePage):
    PRODUCT_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    PRODUCT_BOLT_T_SHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    PRODUCT_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")
    SHOPPING_CART_ICON = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "inventory.html"

    def add_item_to_cart(self, item_locator):
        self.click_element(item_locator)

    def go_to_cart(self):
        self.click_element(self.SHOPPING_CART_ICON)