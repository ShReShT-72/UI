import allure
import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.constants import (
    CHECKOUT_COMPLETE_TEXT,
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    URL_CHECKOUT_STEP_ONE,
    URL_CHECKOUT_STEP_TWO,
    URL_CHECKOUT_COMPLETE,
    URL_CART,
)
from utils.test_data import CheckoutDataFactory


@allure.feature("Checkout")
class TestCheckout:

    def _navigate_to_checkout(
        self, inventory: InventoryPage, cart: CartPage
    ) -> CheckoutPage:
        inventory.open_cart()
        cart.open_checkout()
        return CheckoutPage(inventory.page, inventory.config, inventory.logger)

    @allure.title("Full checkout flow completes successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.checkout
    @pytest.mark.smoke
    def test_complete_successful_checkout(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate to checkout"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
            assert logged_in_page.page.url == URL_CHECKOUT_STEP_ONE

        with allure.step("Fill checkout details with generated data"):
            data = CheckoutDataFactory().generate_checkout_information()
            checkout.fill_checkout_details(data["first_name"], data["last_name"], data["postal_code"])
            checkout.continue_checkout()

        with allure.step("Finish checkout and assert confirmation"):
            checkout.finish_checkout()
            assert logged_in_page.page.url == URL_CHECKOUT_COMPLETE
            assert checkout.is_order_complete()
            assert checkout.get_order_confirmation() == CHECKOUT_COMPLETE_TEXT

    @allure.title("Submitting empty checkout form shows first name error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_empty_checkout_form_shows_error(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate to checkout"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
        with allure.step("Submit form without filling details"):
            checkout.continue_checkout()
        with allure.step("Assert first name validation error"):
            assert "Error: First Name is required" in checkout.get_error_message()

    @allure.title("Missing last name shows last name required error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_missing_last_name_shows_error(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate to checkout"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
        with allure.step("Fill only first name and submit"):
            checkout.fill_checkout_details("John", "", "")
            checkout.continue_checkout()
        with allure.step("Assert last name required error"):
            assert "Error: Last Name is required" in checkout.get_error_message()

    @allure.title("Missing postal code shows postal code required error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_missing_postal_code_shows_error(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate to checkout"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
        with allure.step("Fill first and last name but not postal code"):
            checkout.fill_checkout_details("John", "Doe", "")
            checkout.continue_checkout()
        with allure.step("Assert postal code required error"):
            assert "Error: Postal Code is required" in checkout.get_error_message()

    @allure.title("Checkout step 2 shows order summary with correct URL")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_checkout_step_two_shows_summary(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate through step 1"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
            data = CheckoutDataFactory().generate_checkout_information()
            checkout.fill_checkout_details(data["first_name"], data["last_name"], data["postal_code"])
            checkout.continue_checkout()
        with allure.step("Assert step 2 URL and summary is visible"):
            assert logged_in_page.page.url == URL_CHECKOUT_STEP_TWO
            assert checkout.is_on_step_two()

    @allure.title("Cancel on checkout step 1 returns to cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_cancel_checkout_returns_to_cart(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate to checkout"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
        with allure.step("Click cancel"):
            checkout.click_cancel()
        with allure.step("Assert redirected back to cart"):
            assert logged_in_page.page.url == URL_CART

    @allure.title("Checkout with multiple items completes successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_checkout_with_multiple_items(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add multiple products and navigate to checkout"):
            logged_in_page.add_products([PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT])
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
        with allure.step("Fill checkout details and proceed"):
            data = CheckoutDataFactory().generate_checkout_information()
            checkout.fill_checkout_details(data["first_name"], data["last_name"], data["postal_code"])
            checkout.continue_checkout()
            checkout.finish_checkout()
        with allure.step("Assert order is complete"):
            assert checkout.is_order_complete()
            assert checkout.get_order_confirmation() == CHECKOUT_COMPLETE_TEXT

    @allure.title("Order summary total is displayed on step 2")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_order_summary_total_displayed(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product and navigate to step 2"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            checkout = self._navigate_to_checkout(logged_in_page, cart_page)
            data = CheckoutDataFactory().generate_checkout_information()
            checkout.fill_checkout_details(data["first_name"], data["last_name"], data["postal_code"])
            checkout.continue_checkout()
        with allure.step("Assert item total and order total are visible"):
            assert "$" in checkout.get_summary_item_total()
            assert "$" in checkout.get_summary_total()
