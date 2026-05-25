import allure
import pytest
from pages.inventory_page import InventoryPage
from utils.assertions import SoftAssertions
from utils.constants import (
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    PRODUCT_BOLT_TSHIRT,
    EXPECTED_PRICES,
    URL_INVENTORY,
    TOTAL_PRODUCT_COUNT,
)


@allure.feature("Inventory")
class TestInventory:

    @allure.title("Add single product updates cart badge to 1")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.inventory
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, logged_in_page: InventoryPage):
        with allure.step(f"Add '{PRODUCT_BACKPACK}' to cart"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
        with allure.step("Assert cart badge shows 1"):
            assert logged_in_page.get_cart_count() == "1"
            assert logged_in_page.page.url == URL_INVENTORY

    @allure.title("Add multiple products updates cart badge correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_add_multiple_products(self, logged_in_page: InventoryPage):
        products = [PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT, PRODUCT_BOLT_TSHIRT]
        with allure.step(f"Add {len(products)} products to cart"):
            logged_in_page.add_products(products)
        with allure.step("Assert cart badge matches product count"):
            assert logged_in_page.get_cart_count() == str(len(products))

    @allure.title("Remove product decrements cart badge correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_remove_product_from_inventory(self, logged_in_page: InventoryPage):
        with allure.step("Add two products"):
            logged_in_page.add_products([PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT])
        with allure.step(f"Remove '{PRODUCT_BIKE_LIGHT}'"):
            logged_in_page.remove_product_by_name(PRODUCT_BIKE_LIGHT)
        with allure.step("Assert cart count is 1 and product is removed"):
            assert logged_in_page.get_cart_count() == "1"
            assert not logged_in_page.is_product_in_cart(PRODUCT_BIKE_LIGHT)

    @allure.title("Product prices match expected values")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_validate_product_prices(self, logged_in_page: InventoryPage, soft: SoftAssertions):
        with allure.step("Fetch all product prices from inventory"):
            product_prices = logged_in_page.get_product_prices()
        with allure.step("Assert each expected price matches"):
            for name, expected_price in EXPECTED_PRICES.items():
                soft.assert_equal(
                    product_prices.get(name),
                    expected_price,
                    f"Price for '{name}'",
                )

    @allure.title("Products sort A-Z correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_products_a_to_z(self, logged_in_page: InventoryPage):
        with allure.step("Sort inventory A to Z"):
            logged_in_page.sort_by("az")
        with allure.step("Assert product names are in ascending alphabetical order"):
            names = logged_in_page.get_product_names()
            assert names == sorted(names), f"Expected A-Z order, got: {names}"

    @allure.title("Products sort Z-A correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_products_z_to_a(self, logged_in_page: InventoryPage):
        with allure.step("Sort inventory Z to A"):
            logged_in_page.sort_by("za")
        with allure.step("Assert product names are in descending alphabetical order"):
            names = logged_in_page.get_product_names()
            assert names == sorted(names, reverse=True), f"Expected Z-A order, got: {names}"

    @allure.title("Products sort low to high price correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_products_price_low_to_high(self, logged_in_page: InventoryPage):
        with allure.step("Sort inventory by price low to high"):
            logged_in_page.sort_by("lohi")
        with allure.step("Assert prices are in ascending order"):
            prices = logged_in_page.get_all_prices_as_float()
            assert prices == sorted(prices), f"Expected low-to-high order, got: {prices}"

    @allure.title("Products sort high to low price correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_sort_products_price_high_to_low(self, logged_in_page: InventoryPage):
        with allure.step("Sort inventory by price high to low"):
            logged_in_page.sort_by("hilo")
        with allure.step("Assert prices are in descending order"):
            prices = logged_in_page.get_all_prices_as_float()
            assert prices == sorted(prices, reverse=True), f"Expected high-to-low order, got: {prices}"

    @allure.title("Inventory page displays correct total product count")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_total_product_count(self, logged_in_page: InventoryPage):
        with allure.step(f"Assert {TOTAL_PRODUCT_COUNT} products are displayed"):
            assert logged_in_page.get_product_count() == TOTAL_PRODUCT_COUNT

    @allure.title("Product description is visible on inventory page")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_product_description_visible(self, logged_in_page: InventoryPage):
        with allure.step(f"Assert '{PRODUCT_BACKPACK}' has a non-empty description"):
            description = logged_in_page.get_product_description(PRODUCT_BACKPACK)
            assert len(description) > 0, "Product description should not be empty"

    @allure.title("Product image is visible on inventory page")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_product_image_visible(self, logged_in_page: InventoryPage):
        with allure.step(f"Assert '{PRODUCT_BACKPACK}' image is visible"):
            assert logged_in_page.is_product_image_visible(PRODUCT_BACKPACK)

    @allure.title("Clicking product name navigates to product detail page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_product_detail_page_navigation(self, logged_in_page: InventoryPage):
        with allure.step(f"Click on '{PRODUCT_BACKPACK}' name"):
            logged_in_page.click_product_name(PRODUCT_BACKPACK)
        with allure.step("Assert URL navigates to product detail page"):
            assert "inventory-item.html" in logged_in_page.page.url

    @allure.title("Adding all products updates cart badge to total count")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_add_all_products_to_cart(self, logged_in_page: InventoryPage):
        with allure.step("Add all available products to cart"):
            count = logged_in_page.add_all_products()
        with allure.step("Assert cart badge equals total product count"):
            assert logged_in_page.get_cart_count() == str(count)

    @allure.title("Cart badge disappears after removing all products")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.inventory
    @pytest.mark.regression
    def test_cart_badge_disappears_when_empty(self, logged_in_page: InventoryPage):
        with allure.step("Add then remove a product"):
            logged_in_page.add_product_by_name(PRODUCT_BACKPACK)
            logged_in_page.remove_product_by_name(PRODUCT_BACKPACK)
        with allure.step("Assert cart badge is gone and count is 0"):
            assert logged_in_page.get_cart_count() == "0"
