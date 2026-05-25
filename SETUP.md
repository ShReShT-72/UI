# One-Time Setup Guide

Complete setup instructions for getting this framework running from scratch on a new machine.
Follow every step in order — each one only needs to be done once.

---

## Prerequisites

| Requirement | Version  | Download |
|-------------|----------|----------|
| Python      | 3.11+    | https://www.python.org/downloads/ |
| Git         | Any      | https://git-scm.com/downloads |
| Java (for Allure CLI) | 8+ | https://adoptium.net/ |
| Allure CLI  | 2.x      | https://github.com/allure-framework/allure2/releases |

> Java is only required to run `allure serve`. The tests themselves do not need Java.

---

## Step 1 — Clone the Repository

```bash
git clone <repo-url>
cd project_root
```

---

## Step 2 — Create a Virtual Environment

Always use a virtual environment to keep project dependencies isolated.

```bash
python -m venv .venv
```

**Activate it:**

```bash
# Windows (Command Prompt / PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

You will see `(.venv)` in your terminal prompt when it is active.

> You need to activate the venv every time you open a new terminal session.

---

## Step 3 — Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## Step 4 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs: `pytest`, `playwright`, `allure-pytest`, `pytest-xdist`, `pytest-html`,
`pytest-rerunfailures`, `faker`, `python-dotenv`, `ruff`, and `pre-commit`.

---

## Step 5 — Install Playwright Browser

```bash
python -m playwright install chromium
```

To install all browsers (optional):
```bash
python -m playwright install
```

---

## Step 6 — Install Pre-commit Hooks

```bash
pre-commit install
```

This sets up automatic `ruff` linting and formatting on every `git commit`.

To run manually across all files at any time:
```bash
pre-commit run --all-files
```

---

## Step 7 — Configure Secrets

Create the file `config/.env` with the following content:

```
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

> Never commit this file. It is already listed in `.gitignore`.

---

## Step 8 — Install Allure CLI (for Allure reports)

### Windows

**Option A — Scoop (recommended):**
```bash
scoop install allure
```

**Option B — Manual:**
1. Download the latest zip from https://github.com/allure-framework/allure2/releases
2. Extract it to a folder e.g. `C:\allure`
3. Add `C:\allure\bin` to your system `PATH`
4. Restart your terminal and verify: `allure --version`

### macOS

```bash
brew install allure
```

### Linux

```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

---

## Step 9 — Configure VS Code Interpreter

If you are using VS Code, point Pylance to the `.venv` interpreter so imports resolve correctly:

1. Press `Ctrl+Shift+P`
2. Type `Python: Select Interpreter`
3. Choose the entry showing `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux)

This is already pre-configured in `.vscode/settings.json` — VS Code should pick it up automatically.

---

## Verify Everything Works

Run this to confirm the full setup is correct:

```bash
# Activate venv first
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# Check Python and key packages
python --version
python -m pytest --version
python -m playwright --version
allure --version

# Run smoke tests to verify end-to-end
pytest -m smoke
```

All smoke tests should pass. If they do, the setup is complete.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: playwright` | Run `pip install -r requirements.txt` inside the activated venv |
| `playwright: command not found` | Use `python -m playwright` instead |
| `allure: command not found` | Allure CLI is not on PATH — see Step 8 |
| Pylance shows import errors | Select the `.venv` interpreter in VS Code — see Step 9 |
| Tests fail with `Missing required config keys` | Check that `config/.env` exists and has all required keys |
| Browser does not open in headed mode | Ensure `HEADLESS=false` in `.env` or use `--env dev` |

---

## Daily Workflow

After the one-time setup above, your daily workflow is just:

```bash
# 1. Activate venv
.venv\Scripts\activate

# 2. Run tests
python run_tests.py

# 3. View Allure report
allure serve allure-results
```
