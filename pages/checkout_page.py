from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
import logging


class CheckoutPage(BasePage):
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    FINISH_BUTTON = "#finish"
    COMPLETE_HEADER = ".complete-header"
    ERROR_MESSAGE = "h3[data-test=error]"

    def __init__(self, page: Page, config: ConfigReader, logger: logging.Logger) -> None:
        super().__init__(page, config, logger)

    def fill_checkout_details(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTAL_CODE, postal_code)

    def continue_checkout(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    def finish_checkout(self) -> None:
        self.click(self.FINISH_BUTTON)

    def get_order_confirmation(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_order_complete(self) -> bool:
        return self.is_visible(self.COMPLETE_HEADER, timeout=5000)

    def get_summary_total(self) -> str:
        return self.get_text(".summary_total_label")

    def get_summary_item_total(self) -> str:
        return self.get_text(".summary_subtotal_label")

    def click_cancel(self) -> None:
        self.click("#cancel")

    def is_on_step_two(self) -> bool:
        return self.is_visible(".summary_info")
