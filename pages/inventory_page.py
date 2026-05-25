from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
import logging


class InventoryPage(BasePage):
    TITLE = "span.title"
    CART_LINK = "a.shopping_cart_link"
    CART_BADGE = "span.shopping_cart_badge"
    PRODUCT_CARD = ".inventory_item"
    PRICE_LABEL = ".inventory_item_price"

    SORT_DROPDOWN = ".product_sort_container"

    def __init__(self, page: Page, config: ConfigReader, logger: logging.Logger) -> None:
        super().__init__(page, config, logger)

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def get_page_title(self) -> str:
        return self.get_text(self.TITLE)

    def get_product_locator(self, product_name: str) -> Locator:
        return self.page.locator(f".inventory_item:has-text(\"{product_name}\")")

    def add_product_by_name(self, product_name: str) -> None:
        btn = self.get_product_locator(product_name).locator("button:has-text(\"Add to cart\")")
        btn.wait_for(state="visible", timeout=self.timeout)
        self.logger.info(f"Adding product to cart: {product_name}")
        btn.click()

    def add_products(self, product_names: list[str]) -> None:
        for name in product_names:
            self.add_product_by_name(name)

    def remove_product_by_name(self, product_name: str) -> None:
        btn = self.get_product_locator(product_name).locator("button:has-text(\"Remove\")")
        btn.wait_for(state="visible", timeout=self.timeout)
        self.logger.info(f"Removing product from cart: {product_name}")
        btn.click()

    def get_product_price(self, product_name: str) -> str:
        product_card = self.get_product_locator(product_name)
        return product_card.locator(self.PRICE_LABEL).text_content().strip()

    def get_product_prices(self) -> dict[str, str]:
        items = self.page.locator(self.PRODUCT_CARD)
        prices: dict[str, str] = {}
        for item in items.all():
            title = item.locator(".inventory_item_name").text_content().strip()
            price = item.locator(self.PRICE_LABEL).text_content().strip()
            prices[title] = price
        return prices

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def get_cart_count(self) -> str:
        if self.is_visible(self.CART_BADGE, timeout=1000):
            return self.get_text(self.CART_BADGE)
        return "0"

    def sort_by(self, option: str) -> None:
        """
        Sort inventory by option value.
        Options: 'az' | 'za' | 'lohi' | 'hilo'
        """
        self.logger.info(f"Sorting inventory by: {option}")
        self.page.locator(self.SORT_DROPDOWN).select_option(option)

    def get_product_names(self) -> list[str]:
        return [
            name.strip()
            for name in self.page.locator(".inventory_item_name").all_text_contents()
        ]

    def get_all_prices_as_float(self) -> list[float]:
        return [
            float(p.strip().replace("$", ""))
            for p in self.page.locator(self.PRICE_LABEL).all_text_contents()
        ]

    def is_product_in_cart(self, product_name: str) -> bool:
        product_card = self.get_product_locator(product_name)
        return product_card.locator(f"button:has-text(\"Remove\")").is_visible()

    def get_product_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARD).count()

    def get_product_description(self, product_name: str) -> str:
        product_card = self.get_product_locator(product_name)
        return product_card.locator(".inventory_item_desc").text_content().strip()

    def click_product_name(self, product_name: str) -> None:
        self.logger.info(f"Clicking product name: {product_name}")
        self.get_product_locator(product_name).locator(".inventory_item_name").click()

    def is_product_image_visible(self, product_name: str) -> bool:
        product_card = self.get_product_locator(product_name)
        return product_card.locator(".inventory_item_img img").is_visible()

    def add_all_products(self) -> int:
        names = self.get_product_names()
        for name in names:
            self.add_product_by_name(name)
        return len(names)
