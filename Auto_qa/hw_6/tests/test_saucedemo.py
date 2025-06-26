import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestSauceDemo:
    def test_purchase_flow(self, driver):
        # 1. opening the site and authorisation
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")

        # 2. Adding the goods to the cart
        products_page = ProductsPage(driver)
        products_page.add_item_to_cart(products_page.PRODUCT_BACKPACK)
        print("first product succefully added")
        products_page.add_item_to_cart(products_page.PRODUCT_BOLT_T_SHIRT)
        print("second product succefully added")
        products_page.add_item_to_cart(products_page.PRODUCT_ONESIE)
        print("third product succefully added")

        # 3. Heading to the cart
        products_page.go_to_cart()
        print(f"succesfully activated cart, current url={driver.current_url}")

        # 4. Heading to checkout
        cart_page = CartPage(driver)
        cart_page.click_checkout()

        # 5. Filling the checkout form
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_your_information("Test", "User", "12345")

        # 6. Reading the actual sum
        actual_total = checkout_page.get_total_price()
        print(f"\nTotal sum is: {actual_total}")

        # 7. Checking the actual sum
        expected_total = "$58.29"
        assert actual_total == expected_total, \
            f"Expected total sum {expected_total}, but received {actual_total}"
        # 8. Finishing the order
        checkout_page.click_finish()