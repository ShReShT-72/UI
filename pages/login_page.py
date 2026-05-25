from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.constants import BASE_URL
from utils.config_reader import ConfigReader
import logging


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "div.error-message-container h3"
    PAGE_TITLE = "span.title"

    def __init__(self, page: Page, config: ConfigReader, logger: logging.Logger) -> None:
        super().__init__(page, config, logger)

    def open(self) -> None:
        self.navigate_to(self.config.get("base_url", BASE_URL))

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password, sensitive=True)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_login_page_loaded(self) -> bool:
        return self.is_visible(self.USERNAME_INPUT) and self.is_visible(self.PASSWORD_INPUT)

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_username_placeholder(self) -> str:
        return self.get_attribute(self.USERNAME_INPUT, "placeholder")

    def get_password_placeholder(self) -> str:
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder")

    def is_login_button_visible(self) -> bool:
        return self.is_visible(self.LOGIN_BUTTON)
