import allure
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import ConfigReader
from utils.constants import URL_INVENTORY, BASE_URL


@allure.feature("Authentication")
class TestLogin:

    @allure.title("Valid credentials redirect to inventory page")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.login
    @pytest.mark.smoke
    def test_valid_login(self, logged_in_page: InventoryPage):
        with allure.step("Assert inventory page is loaded"):
            assert logged_in_page.is_page_loaded()
            assert logged_in_page.get_page_title() == "Products"
            assert logged_in_page.page.url == URL_INVENTORY

    @allure.title("Invalid credentials show error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_invalid_login(self, login_page: LoginPage, config: ConfigReader):
        with allure.step("Attempt login with invalid credentials"):
            login_page.login(config.get("invalid_user"), config.get("invalid_password"))
        with allure.step("Assert error message is displayed"):
            assert "Username and password do not match" in login_page.get_error_message()

    @allure.title("Locked user is blocked with appropriate error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_locked_user_login(self, login_page: LoginPage, config: ConfigReader):
        with allure.step("Attempt login with locked user"):
            login_page.login(config.get("locked_user"), config.get("password"))
        with allure.step("Assert locked-out error is shown"):
            assert "Sorry, this user has been locked out." in login_page.get_error_message()

    @allure.title("Empty credentials show validation error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_empty_credentials_validation(self, login_page: LoginPage):
        with allure.step("Submit login form with empty fields"):
            login_page.login("", "")
        with allure.step("Assert validation error is shown"):
            error = login_page.get_error_message()
            assert "Username is required" in error or "Password is required" in error

    @allure.title("Empty password field shows password required error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_empty_password_validation(self, login_page: LoginPage, config: ConfigReader):
        with allure.step("Submit with valid username but empty password"):
            login_page.login(config.get("username"), "")
        with allure.step("Assert password required error"):
            assert "Password is required" in login_page.get_error_message()

    @allure.title("Empty username field shows username required error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_empty_username_validation(self, login_page: LoginPage, config: ConfigReader):
        with allure.step("Submit with empty username but valid password"):
            login_page.login("", config.get("password"))
        with allure.step("Assert username required error"):
            assert "Username is required" in login_page.get_error_message()

    @allure.title("Login page UI elements are visible on load")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_page_elements_visible(self, login_page: LoginPage):
        with allure.step("Assert all login form elements are present"):
            assert login_page.is_login_page_loaded()
            assert login_page.is_login_button_visible()

    @allure.title("Login page input placeholders are correct")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_page_placeholders(self, login_page: LoginPage):
        with allure.step("Assert username and password placeholders"):
            assert login_page.get_username_placeholder() == "Username"
            assert login_page.get_password_placeholder() == "Password"

    @allure.title("Failed login keeps user on login page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_failed_login_stays_on_login_page(self, login_page: LoginPage, config: ConfigReader):
        with allure.step("Attempt login with invalid credentials"):
            login_page.login(config.get("invalid_user"), config.get("invalid_password"))
        with allure.step("Assert URL remains on login page"):
            assert login_page.page.url == BASE_URL
