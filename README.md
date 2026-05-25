Playwright Python Automation Framework
====================================

Overview
--------
A production-grade UI and API test automation framework for the Sauce Demo e-commerce application.
Built with Python, Pytest, and Playwright using a Page Object Model architecture.
Supports multi-environment execution, storage-state authentication, Playwright tracing, Allure reporting, parallel test runs, soft assertions, and GitHub Actions CI integration.

Features
--------
- Architecture: Page Object Model (POM)
- Test Runner: Pytest
- Browser Automation: Playwright — Chromium, Firefox, Webkit
- API Testing: Playwright APIRequestContext — HTTP-level test layer
- Auth Strategy: Storage-state session reuse — login once per suite
- Parallel Execution: pytest-xdist with configurable worker count
- Retry on Failure: pytest-rerunfailures + custom @retry decorator
- HTML Reporting: pytest-html with self-contained output
- Allure Reporting: step-by-step results with severity, history, and trends
- Tracing on Failure: Playwright trace zip — open in Trace Viewer
- Screenshots on Failure: auto-captured and embedded in HTML report
- Soft Assertions: collect all failures per test and report together
- Logging: timestamped file + console, configurable log level
- Test Data Generation: Faker library for dynamic data
- Multi-Environment: default / dev / staging config overlays
- Config Management: JSON config + .env overrides with required key validation
- Code Quality: ruff linting + formatting enforced via pre-commit
- CI/CD: GitHub Actions — pip cache, browser cache, all artifacts

Project Structure
-----------------
project_root/
  pages/                    Page Object classes
    base_page.py            Shared base methods (click, fill, wait, etc.)
    login_page.py           Login page interactions
    inventory_page.py       Product listing, sort, and cart actions
    cart_page.py            Cart page interactions
    checkout_page.py        Checkout flow interactions

  tests/                    Test suites
    conftest.py             Test-scoped page object fixtures
    test_login.py           Login scenarios (valid, invalid, locked, empty)
    test_inventory.py       Product add/remove, price validation, sort
    test_cart.py            Cart contents and navigation
    test_checkout.py        End-to-end checkout flow
    test_api.py             API-level HTTP tests (status, headers, auth)

  utils/                    Shared utilities
    api_client.py           Playwright APIRequestContext wrapper
    assertions.py           Soft assertions — collect all failures per test
    config_reader.py        Multi-env config loader with .env override
    constants.py            URLs, titles, product names, prices
    logger.py               Configurable timestamped logger
    retry.py                @retry decorator for flaky operations
    screenshots.py          Screenshot capture helper
    test_data.py            Faker-based dynamic test data generation

  config/                   Configuration files and runtime overrides
    config.json             Base framework settings
    config.dev.json         Dev environment overrides
    config.staging.json     Staging environment overrides
    .env                    Secrets and runtime overrides (not committed)

  reports/                  Generated HTML test reports
  logs/                     Timestamped execution logs
  screenshots/              Failure screenshots
  traces/                   Playwright trace zips (failure only)
  allure-results/           Raw Allure result data

  .github/workflows/        GitHub Actions CI pipeline
    playwright.yml
  .gitignore                Excludes secrets, output dirs, caches
  .pre-commit-config.yaml   Pre-commit hooks (ruff lint + format)
  .vscode/settings.json     VS Code interpreter configuration
  ruff.toml                 Ruff linter configuration
  conftest.py               Root fixtures: browser, auth state, tracing
  pytest.ini                Pytest config, markers, allure dir
  requirements.txt          Pinned Python dependencies
  run_tests.py              Entry point with env support and reporting
  SETUP.md                  One-time setup guide
  README.md

Installation
------------
1. Clone the repository:
   git clone <repo-url>
   cd project_root

2. Create and activate a virtual environment:
   python -m venv .venv

   Windows:
     .venv\Scripts\activate
   macOS / Linux:
     source .venv/bin/activate

3. Install Python dependencies:
   python -m pip install --upgrade pip
   pip install -r requirements.txt

4. Install Playwright browser:
   python -m playwright install chromium

5. Install pre-commit hooks:
   pre-commit install

6. Configure secrets:
   Create config/.env with the following content:
     ENV=default
     BROWSER=chromium
     HEADLESS=true
     TIMEOUT=10000
     RETRY=1
     LOG_LEVEL=INFO
     APP_USERNAME=standard_user
     APP_PASSWORD=secret_sauce
     APP_LOCKED_USER=locked_out_user
     APP_INVALID_USER=invalid_user
     APP_INVALID_PASSWORD=wrong_password

Notes:
- config/.env is ignored by git and must never be committed.

Configuration
-------------
Environment Strategy:
- config/config.json: Base defaults for all environments
- config/config.dev.json: Dev overrides — headless=false, workers=1, retry=0
- config/config.staging.json: Staging overrides — longer timeouts, more retries
- config/.env: Secrets and runtime overrides — never commit

Base Config (config/config.json):
  {
    "base_url": "https://www.saucedemo.com/",
    "browser": "chromium",
    "headless": true,
    "timeout": 10000,
    "retry": 1,
    "workers": 2
  }

Running Tests
-------------
Activate the virtual environment before running commands.

Full suite with HTML report and Allure results:
  python run_tests.py

Against a specific environment:
  python run_tests.py --env dev
  python run_tests.py --env staging

Via pytest directly:
  pytest

Run a specific file or test:
  pytest tests/test_login.py
  pytest tests/test_checkout.py -k "test_complete_successful_checkout"

By marker:
  pytest -m smoke
  pytest -m regression
  pytest -m api
  pytest -m login
  pytest -m "cart or checkout"

Specific browser:
  pytest --browser-name firefox
  pytest --browser-name webkit

Headed mode (visible browser window):
  pytest --env dev

Quick Reference
---------------
- Full suite + report: python run_tests.py
- Smoke tests only: pytest -m smoke
- API tests only: pytest -m api
- Regression suite: pytest -m regression
- Headed browser: pytest --env dev
- Specific test by name: pytest -k "test_name"
- Firefox browser: pytest --browser-name firefox
- View Allure report: allure serve allure-results
- View failure trace: playwright show-trace traces/<trace-file>.zip
- Lint and format: pre-commit run --all-files

Parallel Execution
------------------
  pytest -n auto
  pytest -n 4

Worker count can also be controlled via the workers key in config.json when running python run_tests.py.

Reporting
---------
HTML Report:
- run_tests.py produces a report in reports/playwright_report_<timestamp>.html
- pytest directly produces reports/report.html

Allure Report:
  allure serve allure-results

If allure is not installed, install the Allure CLI. See SETUP.md for platform-specific instructions.

API Testing
------------
The framework includes a dedicated API test layer using Playwright's built-in APIRequestContext.
These tests validate HTTP responses directly — no browser, no UI — making them faster than UI tests.

Run API-only tests:
  pytest -m api

Run smoke suite with API and UI critical path:
  pytest -m smoke

What the API tests cover:
- App and page reachability (HTTP 200 checks)
- Static asset delivery (CSS, favicon)
- Auth-gated page protection
- Response header validation
- Hybrid API health check before UI suite runs

Soft Assertions
---------------
Use the soft fixture to collect multiple assertion failures within a single test instead of stopping at the first one.
Available methods: assert_equal, assert_true, assert_false, assert_in.

Retry Decorator
---------------
Use @retry on flaky utility functions to retry on failure.

Tracing on Failure
------------------
When a test fails, a Playwright trace zip is saved to traces/.
Open it with:
  playwright show-trace traces/<trace-file>.zip

Authentication Strategy
-----------------------
Login is performed once per test session using Playwright storage state.
Session cookies are saved and reused so tests do not repeat login UI steps.

Logging and Screenshots
-----------------------
- Logs: logs/<timestamp>.log
- Screenshots: screenshots/<test-name>.png
- Traces: traces/<trace-file>.zip

Test Markers
------------
- smoke: Critical path — run on every commit
- regression: Full suite — run nightly
- api: API-level HTTP tests — no browser required
- login: Login page scenarios
- inventory: Product listing, cart actions, sort
- cart: Cart page interactions
- checkout: End-to-end checkout flow
- slow: Tests exceeding 10 seconds

Code Quality
------------
Pre-commit hooks run automatically on every git commit.
Run manually:
  pre-commit run --all-files

CI/CD — GitHub Actions
----------------------
Workflow file: .github/workflows/playwright.yml
Triggers: push to main, pull requests

Pipeline steps:
- Checkout repository
- Set up Python 3.11
- Restore pip cache keyed on requirements.txt
- Restore Playwright browser cache
- Install Python dependencies
- Install Playwright Chromium
- Run the test suite via python run_tests.py
- Upload HTML report artifact
- Upload Allure results artifact
- Upload failure traces

GitHub secrets and variables should be configured in the repository settings for credentials and environment selection.

Notes
-----
- Replace the badge URLs in README.md with your actual GitHub repository path.
- Tests target https://www.saucedemo.com/.
- Never commit config/.env.
- For cross-browser runs use --browser-name firefox or --browser-name webkit.
- See SETUP.md for a complete one-time setup guide.
