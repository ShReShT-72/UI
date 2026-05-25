from __future__ import annotations

import pytest
from pathlib import Path
from typing import TYPE_CHECKING
from utils.config_reader import ConfigReader
from utils.logger import get_logger
from utils.screenshots import save_screenshot
from utils.assertions import SoftAssertions

if TYPE_CHECKING:
    from playwright.sync_api import Browser, BrowserContext


# ---------------------------------------------------------------------------
# CLI options
# ---------------------------------------------------------------------------

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser-name", action="store", default=None,
                     help="Browser: chromium | firefox | webkit")
    parser.addoption("--env", action="store", default=None,
                     help="Environment: default | dev | staging")


# ---------------------------------------------------------------------------
# Session-scoped core fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config(request) -> ConfigReader:
    env = request.config.getoption("--env")
    return ConfigReader(env=env)


@pytest.fixture(scope="session")
def logger(config: ConfigReader):
    return get_logger("automation")


@pytest.fixture(scope="session")
def playwright_instance():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance, config: ConfigReader, request) -> Browser:
    browser_name = request.config.getoption("--browser-name") or config.get_browser()
    if browser_name not in ("chromium", "firefox", "webkit"):
        browser_name = "chromium"
    headless = config.get("headless", True)
    _browser = getattr(playwright_instance, browser_name).launch(headless=headless)
    yield _browser
    _browser.close()


# ---------------------------------------------------------------------------
# Storage-state auth: log in once per session, reuse cookie state
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def auth_state(browser, config: ConfigReader, logger, tmp_path_factory) -> Path:
    """
    Performs a real login once, saves browser storage state to a temp file,
    and returns the path. All tests reuse this state — no repeated UI logins.
    """
    from pages.login_page import LoginPage

    state_file = tmp_path_factory.mktemp("auth") / "storage_state.json"
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(config.get("timeout", 10000))

    login_page = LoginPage(page, config, logger)
    login_page.open()
    login_page.login(config.get("username"), config.get("password"))
    page.wait_for_url("**/inventory.html", timeout=config.get("timeout", 10000))

    context.storage_state(path=str(state_file))
    context.close()
    logger.info(f"Auth storage state saved to: {state_file}")
    return state_file


# ---------------------------------------------------------------------------
# Per-test page fixture with tracing
# ---------------------------------------------------------------------------

@pytest.fixture()
def context(browser, config: ConfigReader, auth_state: Path) -> BrowserContext:
    """Creates a fresh browser context pre-loaded with saved auth state."""
    ctx = browser.new_context(storage_state=str(auth_state))
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    ctx.tracing.stop()  # discard trace if test passed (saved only on failure via hook)
    ctx.close()


@pytest.fixture()
def page(context: BrowserContext, config: ConfigReader):
    _page = context.new_page()
    _page.set_default_timeout(config.get("timeout", 10000))
    yield _page


@pytest.fixture()
def logged_in_page(page, config: ConfigReader, logger):
    """
    Returns an InventoryPage already at /inventory.html via storage state auth.
    No UI login performed — uses saved session cookies.
    """
    from pages.inventory_page import InventoryPage
    from utils.constants import URL_INVENTORY

    page.goto(URL_INVENTORY, timeout=config.get("timeout", 10000))
    return InventoryPage(page, config, logger)


@pytest.fixture()
def soft() -> SoftAssertions:
    """Soft assertions — collects all failures and reports them together at teardown."""
    sa = SoftAssertions()
    yield sa
    sa.assert_all()


# ---------------------------------------------------------------------------
# API client fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def api_client(playwright_instance, config: ConfigReader, logger):
    """
    Session-scoped Playwright APIRequestContext.
    Use this for API-level tests and hybrid UI+API tests.
    """
    from utils.api_client import APIClient
    base_url = config.get("base_url", "https://www.saucedemo.com")
    request_context = playwright_instance.request.new_context(base_url=base_url)
    yield APIClient(request_context, base_url, logger)
    request_context.dispose()


# ---------------------------------------------------------------------------
# Failure hook: save screenshot + trace on test failure
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    funcargs = getattr(item, "funcargs", {})
    _page = funcargs.get("page")
    _context = funcargs.get("context")

    if _page is None:
        return

    # Screenshot
    screenshot_path = save_screenshot(_page, item.name)

    # Trace
    traces_dir = Path(__file__).resolve().parent / "traces"
    traces_dir.mkdir(exist_ok=True)
    trace_path = traces_dir / f"{item.name}.zip"
    try:
        _context.tracing.stop(path=str(trace_path))
    except Exception:
        pass

    # Embed screenshot in HTML report
    html = getattr(report, "extra", [])
    try:
        from pytest_html import extras
        html.append(extras.image(str(screenshot_path)))
        html.append(extras.url(str(trace_path), f"Trace: {trace_path.name}"))
        report.extra = html
    except ModuleNotFoundError:
        pass
