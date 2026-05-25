from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
import logging


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    REMOVE_BUTTON = "button:has-text(\"Remove\")"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page: Page, config: ConfigReader, logger: logging.Logger) -> None:
        super().__init__(page, config, logger)

    def get_cart_items(self) -> list[str]:
        return [
            name.strip()
            for name in self.page.locator(f"{self.CART_ITEM} {self.ITEM_NAME}").all_text_contents()
        ]

    def verify_item_in_cart(self, product_name: str) -> bool:
        return product_name in self.get_cart_items()

    def remove_item(self, product_name: str) -> None:
        item = self.page.locator(f".cart_item:has-text('{product_name}')")
        if not item.is_visible():
            raise ValueError(f"Product '{product_name}' was not found in cart")
        item.locator(self.REMOVE_BUTTON).click()
        self.logger.info(f"Removed item from cart: {product_name}")

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def open_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def get_cart_size(self) -> int:
        return len(self.get_cart_items())

    def is_empty(self) -> bool:
        return self.get_cart_size() == 0

    def get_item_price(self, product_name: str) -> str:
        item = self.page.locator(f".cart_item:has-text('{product_name}')")
        return item.locator(".inventory_item_price").text_content().strip()

    def get_item_quantity(self, product_name: str) -> str:
        item = self.page.locator(f".cart_item:has-text('{product_name}')")
        return item.locator(".cart_quantity").text_content().strip()
