import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils.config_reader import ConfigReader


@pytest.fixture()
def login_page(page, config: ConfigReader, logger) -> LoginPage:
    lp = LoginPage(page, config, logger)
    lp.open()
    return lp


@pytest.fixture()
def cart_page(logged_in_page: InventoryPage) -> CartPage:
    return CartPage(logged_in_page.page, logged_in_page.config, logged_in_page.logger)


@pytest.fixture()
def checkout_page(logged_in_page: InventoryPage) -> CheckoutPage:
    return CheckoutPage(logged_in_page.page, logged_in_page.config, logged_in_page.logger)
