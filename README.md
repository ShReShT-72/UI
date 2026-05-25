# Playwright Python Automation Framework

![CI](https://github.com/<your-username>/<your-repo>/actions/workflows/playwright.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Playwright](https://img.shields.io/badge/playwright-1.40%2B-green?logo=playwright)
![Allure](https://img.shields.io/badge/reporting-allure-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A production-grade UI and API test automation framework for the [Sauce Demo](https://www.saucedemo.com/)
e-commerce application. Built with **Python**, **Pytest**, and **Playwright** using a Page Object Model
architecture. Supports multi-environment execution, storage-state authentication, Playwright tracing,
Allure reporting, parallel test runs, soft assertions, and GitHub Actions CI integration.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Quick Reference](#quick-reference)
- [Parallel Execution](#parallel-execution)
- [Reporting](#reporting)
- [API Testing](#api-testing)
- [Soft Assertions](#soft-assertions)
- [Retry Decorator](#retry-decorator)
- [Tracing on Failure](#tracing-on-failure)
- [Authentication Strategy](#authentication-strategy)
- [Logging and Screenshots](#logging-and-screenshots)
- [Test Markers](#test-markers)
- [Code Quality](#code-quality)
- [CI/CD — GitHub Actions](#cicd--github-actions)
- [Notes](#notes)

---

## Features

| Feature                 | Details                                                   |
|-------------------------|-----------------------------------------------------------|
| Architecture            | Page Object Model (POM)                                   |
| Test Runner             | Pytest                                                    |
| Browser Automation      | Playwright — Chromium, Firefox, Webkit                    |
| API Testing             | Playwright `APIRequestContext` — HTTP-level test layer    |
| Auth Strategy           | Storage-state session reuse — login once per suite        |
| Parallel Execution      | `pytest-xdist` with configurable worker count             |
| Retry on Failure        | `pytest-rerunfailures` + custom `@retry` decorator        |
| HTML Reporting          | `pytest-html` with self-contained output                  |
| Allure Reporting        | Step-by-step results with severity, history, and trends   |
| Tracing on Failure      | Playwright trace zip — open in Trace Viewer               |
| Screenshots on Failure  | Auto-captured and embedded in HTML report                 |
| Soft Assertions         | Collect all failures per test and report together         |
| Logging                 | Timestamped file + console, configurable log level        |
| Test Data Generation    | `Faker` library for dynamic data                          |
| Multi-Environment       | `default` / `dev` / `staging` config overlays             |
| Config Management       | JSON config + `.env` overrides with required key validation|
| Code Quality            | `ruff` linting + formatting enforced via `pre-commit`     |
| CI/CD                   | GitHub Actions — pip cache, browser cache, all artifacts  |

---

## Project Structure

```
project_root/
│
├── pages/                           # Page Object classes
│   ├── base_page.py                 # Shared base methods (click, fill, wait, etc.)
│   ├── login_page.py                # Login page interactions
│   ├── inventory_page.py            # Product listing, sort, and cart actions
│   ├── cart_page.py                 # Cart page interactions
│   └── checkout_page.py            # Checkout flow interactions
│
├── tests/                           # Test suites
│   ├── conftest.py                  # Test-scoped page object fixtures
│   ├── test_login.py                # Login scenarios (valid, invalid, locked, empty)
│   ├── test_inventory.py            # Product add/remove, price validation, sort
│   ├── test_cart.py                 # Cart contents and navigation
│   ├── test_checkout.py            # End-to-end checkout flow
│   └── test_api.py                  # API-level HTTP tests (status, headers, auth)
│
├── utils/                           # Shared utilities
│   ├── api_client.py                # Playwright APIRequestContext wrapper
│   ├── assertions.py                # Soft assertions — collect all failures per test
│   ├── config_reader.py             # Multi-env config loader with .env override
│   ├── constants.py                 # URLs, titles, product names, prices
│   ├── logger.py                    # Configurable timestamped logger
│   ├── retry.py                     # @retry decorator for flaky operations
│   ├── screenshots.py               # Screenshot capture helper
│   └── test_data.py                 # Faker-based dynamic test data generation
│
├── config/
│   ├── config.json                  # Base framework settings
│   ├── config.dev.json              # Dev environment overrides
│   ├── config.staging.json          # Staging environment overrides
│   └── .env                         # Secrets and runtime overrides (not committed)
│
├── reports/                         # Generated HTML test reports
├── logs/                            # Timestamped execution logs
├── screenshots/                     # Failure screenshots
├── traces/                          # Playwright trace zips (failure only)
├── allure-results/                  # Raw Allure result data
│
├── .github/
│   └── workflows/
│       └── playwright.yml           # GitHub Actions CI pipeline
│
├── .gitignore                       # Excludes secrets, output dirs, caches
├── .pre-commit-config.yaml          # Pre-commit hooks (ruff lint + format)
├── .vscode/
│   └── settings.json                # VS Code interpreter configuration
├── ruff.toml                        # Ruff linter configuration
├── conftest.py                      # Root fixtures: browser, auth state, tracing
├── pytest.ini                       # Pytest config, markers, allure dir
├── requirements.txt                 # Pinned Python dependencies
├── run_tests.py                     # Entry point with env support and reporting
├── SETUP.md                         # One-time setup guide
└── README.md
```

---

## Installation

> For the complete one-time setup guide including virtual environment creation,
> VS Code configuration, and Allure CLI installation, see **[SETUP.md](SETUP.md)**.

**1. Clone the repository**

```bash
git clone <repo-url>
cd project_root
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install Python dependencies**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**4. Install Playwright browser**

```bash
python -m playwright install chromium
```

**5. Install pre-commit hooks**

```bash
pre-commit install
```

**6. Configure secrets**

Create `config/.env` with the following content:

```env
# Environment — options: default | dev | staging
ENV=default
BROWSER=chromium
HEADLESS=true
TIMEOUT=10000
RETRY=1
LOG_LEVEL=INFO

# Credentials — prefixed with APP_ to avoid Windows reserved variable conflicts
APP_USERNAME=standard_user
APP_PASSWORD=secret_sauce
APP_LOCKED_USER=locked_out_user
APP_INVALID_USER=invalid_user
APP_INVALID_PASSWORD=wrong_password
```

> `config/.env` is listed in `.gitignore` and must never be committed.

---

## Configuration

### Environment Strategy

| File                         | Purpose                                            |
|------------------------------|----------------------------------------------------|
| `config/config.json`         | Base defaults for all environments                 |
| `config/config.dev.json`     | Dev overrides — headless=false, workers=1, retry=0 |
| `config/config.staging.json` | Staging overrides — longer timeouts, more retries  |
| `config/.env`                | Secrets and runtime overrides — never commit       |

Environment overlays are merged on top of the base config. `.env` values take final precedence.

### Base Config — `config/config.json`

```json
{
  "base_url": "https://www.saucedemo.com/",
  "browser": "chromium",
  "headless": true,
  "timeout": 10000,
  "retry": 1,
  "workers": 2
}
```

---

## Running Tests

> Activate the virtual environment before running any command.
>
> ```bash
> # Windows
> .venv\Scripts\activate
>
> # macOS / Linux
> source .venv/bin/activate
> ```

**Full suite — timestamped HTML report + Allure results:**

```bash
python run_tests.py
```

**Against a specific environment:**

```bash
python run_tests.py --env dev
python run_tests.py --env staging
```

**Via Pytest directly:**

```bash
pytest
```

**Specific file or test:**

```bash
pytest tests/test_login.py
pytest tests/test_checkout.py -k "test_complete_successful_checkout"
```

**By marker:**

```bash
pytest -m smoke        # Critical path — fastest subset
pytest -m regression   # Full suite
pytest -m api          # API tests only — no browser needed
pytest -m login
pytest -m "cart or checkout"
```

**Specific browser:**

```bash
pytest --browser-name firefox
pytest --browser-name webkit
```

**Headed mode — visible browser window:**

```bash
pytest --env dev       # config.dev.json sets headless=false
```

---

## Quick Reference

| Goal                    | Command                                          |
|-------------------------|--------------------------------------------------|
| Full suite + report     | `python run_tests.py`                            |
| Smoke tests only        | `pytest -m smoke`                                |
| API tests only          | `pytest -m api`                                  |
| Regression suite        | `pytest -m regression`                           |
| Headed browser          | `pytest --env dev`                               |
| Specific test by name   | `pytest -k "test_name"`                          |
| Firefox browser         | `pytest --browser-name firefox`                  |
| View Allure report      | `allure serve allure-results`                    |
| View failure trace      | `playwright show-trace traces/<name>.zip`        |
| Lint and format         | `pre-commit run --all-files`                     |

---

## Parallel Execution

```bash
pytest -n auto    # Auto-detect CPU workers
pytest -n 4       # Explicit worker count
```

Worker count is also controlled via the `workers` key in `config.json` when running
`python run_tests.py`.

---

## Reporting

### HTML Report

| Run Method            | Report Location                                |
|-----------------------|------------------------------------------------|
| `python run_tests.py` | `reports/playwright_report_<timestamp>.html`   |
| `pytest` directly     | `reports/report.html`                          |

Reports are fully self-contained — no external assets required. Failure screenshots are
embedded directly in the report.

### Allure Report

```bash
allure serve allure-results
```

Allure provides step-by-step test breakdowns, severity levels, pass/fail trends over time,
and embedded screenshots per test.

> If the `allure` command is not found, install the Allure CLI.
> See **[SETUP.md](SETUP.md)** for platform-specific instructions.

---

## API Testing

The framework includes a dedicated API test layer using Playwright's built-in
`APIRequestContext`. These tests validate HTTP responses directly — no browser, no UI —
making them significantly faster than UI tests.

```bash
pytest -m api          # Run only API tests
pytest -m smoke        # Run smoke suite (includes API + UI critical path)
```

The `api_client` fixture is session-scoped and available to all tests. It can also be used
in hybrid tests to set up state via API before asserting through the UI.

**What the API tests cover:**

- App and page reachability (HTTP 200 checks)
- Static asset delivery (CSS, favicon)
- Auth-gated page protection
- Response header validation
- Hybrid API health check before UI suite runs

---

## Soft Assertions

Use the `soft` fixture to collect multiple assertion failures within a single test
instead of stopping at the first one. All failures are reported together at teardown.

```python
def test_example(self, soft):
    soft.assert_equal(actual, expected, "field label")
    soft.assert_true(condition, "condition label")
    soft.assert_in(item, collection, "collection label")
    # All failures reported together at end of test
```

Available methods: `assert_equal`, `assert_true`, `assert_false`, `assert_in`.

---

## Retry Decorator

Use `@retry` on any flaky utility function to automatically retry on failure:

```python
from utils.retry import retry

@retry(times=3, delay=1.0, exceptions=(TimeoutError,))
def fetch_data():
    ...
```

Each failed attempt is logged with the attempt number and exception message.

---

## Tracing on Failure

When a test fails, a Playwright trace zip is automatically saved to `traces/<test_name>.zip`.

Open it with:

```bash
playwright show-trace traces/<test_name>.zip
```

The Trace Viewer shows every click, network request, DOM snapshot, and console log
for the failed test — making root cause analysis fast and precise.

---

## Authentication Strategy

Login is performed **once per test session** using Playwright's storage state API.
Session cookies are saved to a temporary file and injected into every subsequent browser
context — no repeated UI logins across the suite.

This eliminates login as a source of flakiness and significantly reduces total suite runtime.

---

## Logging and Screenshots

| Output        | Location                                      | Details                              |
|---------------|-----------------------------------------------|--------------------------------------|
| Logs          | `logs/<name>_<timestamp>.log`                 | Level set via `LOG_LEVEL` in `.env`  |
| Screenshots   | `screenshots/<test_name>_<timestamp>.png`     | Captured on failure, embedded in HTML report |
| Traces        | `traces/<test_name>.zip`                      | Saved on failure, open in Trace Viewer |

---

## Test Markers

| Marker       | Covers                                          |
|--------------|-------------------------------------------------|
| `smoke`      | Critical path — run on every commit (~5 tests)  |
| `regression` | Full suite — run nightly                        |
| `api`        | API-level HTTP tests — no browser required      |
| `login`      | Login page scenarios                            |
| `inventory`  | Product listing, cart actions, sort             |
| `cart`       | Cart page interactions                          |
| `checkout`   | End-to-end checkout flow                        |
| `slow`       | Tests exceeding 10 seconds                      |

---

## Code Quality

Pre-commit hooks run automatically on every `git commit`:

```bash
pre-commit run --all-files    # Run manually across all files
```

| Hook                  | Purpose                                      |
|-----------------------|----------------------------------------------|
| `ruff`                | Linting with auto-fix                        |
| `ruff-format`         | Code formatting                              |
| `trailing-whitespace` | Remove trailing whitespace                   |
| `end-of-file-fixer`   | Ensure files end with a newline              |
| `check-yaml`          | Validate YAML syntax                         |
| `check-json`          | Validate JSON syntax                         |
| `detect-private-key`  | Prevent accidental secret commits            |

---

## CI/CD — GitHub Actions

Workflow file: `.github/workflows/playwright.yml`

**Triggers:** Push to `main` · Pull Requests

**Pipeline steps:**

| Step | Action                                              |
|------|-----------------------------------------------------|
| 1    | Checkout repository                                 |
| 2    | Set up Python 3.11                                  |
| 3    | Restore pip cache (keyed on `requirements.txt`)     |
| 4    | Restore Playwright browser cache                    |
| 5    | Install Python dependencies                         |
| 6    | Install Playwright Chromium                         |
| 7    | Run test suite via `python run_tests.py`            |
| 8    | Upload HTML report artifact *(always)*              |
| 9    | Upload Allure results artifact *(always)*           |
| 10   | Upload failure traces *(always, ignored if empty)*  |

**Secrets** — set in GitHub repo → Settings → Secrets:

| Secret                | Description               |
|-----------------------|---------------------------|
| `APP_USERNAME`        | Valid test username        |
| `APP_PASSWORD`        | Valid test password        |
| `APP_LOCKED_USER`     | Locked-out test username   |
| `APP_INVALID_USER`    | Invalid test username      |
| `APP_INVALID_PASSWORD`| Invalid test password      |

**Variables** — set in GitHub repo → Settings → Variables:

| Variable   | Description                                  |
|------------|----------------------------------------------|
| `TEST_ENV` | Environment to run — `default` or `staging`  |

---

## Notes

- Replace `<your-username>/<your-repo>` in the badge URLs at the top with your actual GitHub path
- All tests target `https://www.saucedemo.com/`
- Never commit `config/.env` — it is listed in `.gitignore`
- For cross-browser runs use `--browser-name firefox` or `--browser-name webkit`
- For the complete one-time setup guide see **[SETUP.md](SETUP.md)**
#   U I  
 