import allure
import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.constants import (
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    PRODUCT_BOLT_TSHIRT,
    URL_CART,
    URL_INVENTORY,
)


@allure.feature("Cart")
class TestCart:

    @allure.title("Products added on inventory page appear in cart")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.cart
    @pytest.mark.smoke
    def test_verify_cart_contents(self, logged_in_page: InventoryPage, cart_page: CartPage):
        products = [PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT]
        with allure.step("Add products from inventory"):
            logged_in_page.add_products(products)
        with allure.step("Navigate to cart"):
            logged_in_page.open_cart()
        with allure.step("Assert cart URL and contents"):
            assert logged_in_page.page.url == URL_CART
            assert cart_page.get_cart_items() == products

    @allure.title("Removing item from cart empties the cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_remove_item_from_cart(self, logged_in_page: InventoryPage, cart_page: CartPage):
        with allure.step("Add product and navigate to cart"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            logged_in_page.open_cart()
        with allure.step(f"Remove '{PRODUCT_BACKPACK}' from cart"):
            cart_page.remove_item(PRODUCT_BACKPACK)
        with allure.step("Assert cart is empty"):
            assert cart_page.get_cart_size() == 0

    @allure.title("Continue shopping returns to inventory with cart preserved")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_continue_shopping_flow(self, logged_in_page: InventoryPage, cart_page: CartPage):
        with allure.step("Add product and navigate to cart"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            logged_in_page.open_cart()
        with allure.step("Click continue shopping"):
            cart_page.continue_shopping()
        with allure.step("Assert back on inventory with cart count preserved"):
            assert logged_in_page.page.url == URL_INVENTORY
            assert logged_in_page.is_page_loaded()
            assert logged_in_page.get_cart_count() == "1"

    @allure.title("Cart is empty when no products have been added")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_empty_cart_has_no_items(self, logged_in_page: InventoryPage, cart_page: CartPage):
        with allure.step("Navigate to cart without adding any products"):
            logged_in_page.open_cart()
        with allure.step("Assert cart is empty"):
            assert cart_page.is_empty()

    @allure.title("Cart item price matches inventory price")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_item_price_matches_inventory(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Get product price from inventory"):
            inventory_price = logged_in_page.get_product_price(PRODUCT_BACKPACK)
        with allure.step("Add product and navigate to cart"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            logged_in_page.open_cart()
        with allure.step("Assert cart price matches inventory price"):
            assert cart_page.get_item_price(PRODUCT_BACKPACK) == inventory_price

    @allure.title("Cart item quantity defaults to 1")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_item_quantity_is_one(self, logged_in_page: InventoryPage, cart_page: CartPage):
        with allure.step("Add product and navigate to cart"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            logged_in_page.open_cart()
        with allure.step("Assert item quantity is 1"):
            assert cart_page.get_item_quantity(PRODUCT_BACKPACK) == "1"

    @allure.title("Removing one item from multi-item cart keeps remaining items")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_remove_one_item_keeps_others(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add three products and navigate to cart"):
            logged_in_page.add_products([PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT, PRODUCT_BOLT_TSHIRT])
            logged_in_page.open_cart()
        with allure.step(f"Remove '{PRODUCT_BIKE_LIGHT}'"):
            cart_page.remove_item(PRODUCT_BIKE_LIGHT)
        with allure.step("Assert remaining two items are still in cart"):
            items = cart_page.get_cart_items()
            assert PRODUCT_BACKPACK in items
            assert PRODUCT_BOLT_TSHIRT in items
            assert PRODUCT_BIKE_LIGHT not in items

    @allure.title("Cart persists items after navigating back from inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_cart_persists_after_navigation(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        with allure.step("Add product, go to cart, then continue shopping"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            logged_in_page.open_cart()
            cart_page.continue_shopping()
        with allure.step("Navigate back to cart"):
            logged_in_page.open_cart()
        with allure.step("Assert product is still in cart"):
            assert cart_page.verify_item_in_cart(PRODUCT_BACKPACK)
