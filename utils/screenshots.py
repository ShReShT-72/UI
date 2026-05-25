from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page


def save_screenshot(page: Page, name: str) -> Path:
    screenshot_directory = Path(__file__).resolve().parent.parent / "screenshots"
    screenshot_directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = screenshot_directory / f"{name}_{timestamp}.png"
    page.screenshot(path=str(screenshot_file), full_page=True)
    return screenshot_file
