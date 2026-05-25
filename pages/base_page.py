from typing import Optional
from playwright.sync_api import Locator, Page
from utils.config_reader import ConfigReader
import logging


class BasePage:
    def __init__(self, page: Page, config: ConfigReader, logger: logging.Logger) -> None:
        self.page = page
        self.config = config
        self.logger = logger
        self.timeout = self.config.get("timeout", 10000)

    def navigate_to(self, url: str) -> None:
        self.logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, timeout=self.timeout)

    def get_locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.logger.info(f"Clicking element: {selector}")
        locator = self.get_locator(selector)
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.click()

    def fill(self, selector: str, text: str, sensitive: bool = False) -> None:
        display = "***" if sensitive else text
        self.logger.info(f"Filling element: {selector} with text: {display}")
        locator = self.get_locator(selector)
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.fill(text)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        locator = self.get_locator(selector)
        locator.wait_for(state="visible", timeout=timeout or self.timeout)
        return locator.text_content().strip()

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        try:
            locator = self.get_locator(selector)
            locator.wait_for(state="visible", timeout=timeout or self.timeout)
            return True
        except Exception:
            return False

    def get_attribute(self, selector: str, attribute: str) -> str:
        locator = self.get_locator(selector)
        locator.wait_for(state="attached", timeout=self.timeout)
        return locator.get_attribute(attribute) or ""

