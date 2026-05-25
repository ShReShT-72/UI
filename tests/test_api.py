"""
API-level tests using Playwright's APIRequestContext.

These tests validate HTTP responses directly — no browser, no UI.
They run significantly faster than UI tests and serve as a contract
layer between the frontend and backend.
"""
from __future__ import annotations

import time
import allure
import pytest
from utils.api_client import APIClient
from utils.config_reader import ConfigReader
from utils.assertions import SoftAssertions


@allure.feature("API")
class TestAPI:

    # ------------------------------------------------------------------
    # App reachability
    # ------------------------------------------------------------------

    @allure.title("App base URL returns HTTP 200")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_app_is_reachable(self, api_client: APIClient):
        with allure.step("GET base URL and assert 200"):
            response = api_client.get("/")
            APIClient.assert_status(response, 200)

    @allure.title("Inventory page is accessible via HTTP")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_inventory_page_reachable(self, api_client: APIClient):
        with allure.step("GET /inventory.html — auth-gated, expect redirect not server error"):
            response = api_client.get("/inventory.html")
            assert response.status < 500, f"Expected non-server-error, got {response.status}"

    @allure.title("Login page returns HTTP 200")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_login_page_reachable(self, api_client: APIClient):
        with allure.step("GET base URL (login page) and assert 200"):
            response = api_client.get("/")
            APIClient.assert_status(response, 200)

    @allure.title("Cart page is accessible via HTTP")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_cart_page_accessible(self, api_client: APIClient):
        with allure.step("GET /cart.html — auth-gated, expect redirect not server error"):
            response = api_client.get("/cart.html")
            assert response.status < 500, f"Expected non-server-error, got {response.status}"

    @allure.title("Checkout step one page is accessible via HTTP")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_checkout_step_one_accessible(self, api_client: APIClient):
        with allure.step("GET /checkout-step-one.html — expect no server error"):
            response = api_client.get("/checkout-step-one.html")
            assert response.status < 500, f"Expected non-server-error, got {response.status}"

    @allure.title("Checkout step two page is accessible via HTTP")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_checkout_step_two_accessible(self, api_client: APIClient):
        with allure.step("GET /checkout-step-two.html — expect no server error"):
            response = api_client.get("/checkout-step-two.html")
            assert response.status < 500, f"Expected non-server-error, got {response.status}"

    # ------------------------------------------------------------------
    # Static asset delivery
    # ------------------------------------------------------------------

    @allure.title("Static CSS assets are served correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_static_css_assets_served(self, api_client: APIClient, soft: SoftAssertions):
        with allure.step("GET main stylesheet"):
            response = api_client.get("/static/css/main.8a7d64a1.css")
        with allure.step("Assert 200 and correct content-type"):
            soft.assert_equal(response.status, 200, "CSS status")
            content_type = response.headers.get("content-type", "")
            soft.assert_in("text/css", content_type, "CSS content-type")

    @allure.title("JavaScript bundle is served correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_js_bundle_served(self, api_client: APIClient, soft: SoftAssertions):
        with allure.step("GET main JS bundle"):
            response = api_client.get("/static/js/main.bcf4bc5f.js")
        with allure.step("Assert 200 and correct content-type"):
            soft.assert_equal(response.status, 200, "JS status")
            content_type = response.headers.get("content-type", "")
            soft.assert_in("javascript", content_type, "JS content-type")

    @allure.title("App favicon is served")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    @pytest.mark.regression
    def test_favicon_served(self, api_client: APIClient):
        with allure.step("GET favicon.ico"):
            response = api_client.get("/favicon.ico")
            APIClient.assert_ok(response)

    # ------------------------------------------------------------------
    # Response headers
    # ------------------------------------------------------------------

    @allure.title("App sets expected response headers")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_response_headers_present(self, api_client: APIClient, soft: SoftAssertions):
        with allure.step("GET base URL and inspect headers"):
            response = api_client.get("/")
        with allure.step("Assert content-type and cache-control headers are present"):
            headers = {k.lower(): v for k, v in response.headers.items()}
            soft.assert_in("content-type", headers, "content-type header")
            soft.assert_in("cache-control", headers, "cache-control header")

    @allure.title("Response content-length header is present")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    @pytest.mark.regression
    def test_content_length_header_present(self, api_client: APIClient):
        with allure.step("GET base URL and check content-length"):
            response = api_client.get("/")
            headers = {k.lower(): v for k, v in response.headers.items()}
            assert "content-length" in headers, "content-length header should be present"

    # ------------------------------------------------------------------
    # Performance
    # ------------------------------------------------------------------

    @allure.title("App base URL responds within acceptable time")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_response_time_acceptable(self, api_client: APIClient):
        with allure.step("GET base URL and measure response time"):
            start = time.time()
            response = api_client.get("/")
            elapsed = time.time() - start
        with allure.step("Assert response time is under 5 seconds"):
            APIClient.assert_status(response, 200)
            assert elapsed < 5.0, f"Response took {elapsed:.2f}s — expected under 5s"

    # ------------------------------------------------------------------
    # Auth-gated page protection
    # ------------------------------------------------------------------

    @allure.title("Checkout page does not return server error for unauthenticated request")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_checkout_requires_auth(self, api_client: APIClient):
        with allure.step("GET /checkout-step-one.html without auth"):
            response = api_client.get("/checkout-step-one.html")
        with allure.step("Assert response is not a server error"):
            assert response.status < 500, (
                f"Server error on unauthenticated checkout access: {response.status}"
            )

    # ------------------------------------------------------------------
    # Hybrid: API health check → UI smoke
    # ------------------------------------------------------------------

    @allure.title("App is reachable via API before UI tests run")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_api_health_before_ui(self, api_client: APIClient, config: ConfigReader):
        with allure.step("Verify base URL is reachable via HTTP"):
            response = api_client.get("/")
            APIClient.assert_status(response, 200)
        with allure.step("Verify config base_url is set correctly"):
            assert config.get("base_url"), "base_url must be configured"
            assert "saucedemo.com" in config.get("base_url"), "base_url must point to saucedemo"

    @allure.title("All core app pages return non-server-error responses")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_all_pages_reachable(self, api_client: APIClient, soft: SoftAssertions):
        pages = ["/", "/inventory.html", "/cart.html", "/checkout-step-one.html"]
        with allure.step("GET all core pages and assert no 5xx responses"):
            for path in pages:
                response = api_client.get(path)
                soft.assert_true(
                    response.status < 500,
                    f"{path} returned {response.status}"
                )
