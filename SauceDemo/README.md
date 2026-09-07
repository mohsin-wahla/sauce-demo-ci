# SauceDemo Playwright + Pytest + POM

A small UI automation demo for [SauceDemo](https://www.saucedemo.com/) using Python, Playwright, Pytest, and the Page Object Model (POM).

The suite covers a complete purchase journey plus a few negative checks (invalid login and checkout without required customer information).

## Technology stack

- Python 3.10+
- Playwright (Chromium)
- Pytest
- python-dotenv
- pytest-html
- allure-pytest

## Project structure

```text
SauceDemo/
├── pages/                      # Page Object classes (locators + actions)
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── checkout_overview_page.py
├── tests/                      # Pytest test cases
│   ├── test_login.py
│   ├── test_cart.py
│   └── test_checkout.py
├── utils/
│   └── config.py               # BASE_URL, credentials, shared test data
├── conftest.py                 # Browser fixture and page objects
├── requirements.txt
├── pytest.ini
├── .env.example
├── .env                        # Local config (gitignored)
└── README.md
```

## Page Object Model

Tests describe *what* to do. Page Objects describe *how* the UI is used.

```text
Test  →  Page Object (login, add to cart, checkout)
      →  Playwright locators/actions
      →  SauceDemo in Chromium
```

Selectors live in `pages/`. Tests call methods such as `login_page.login(...)` instead of using raw CSS in assertions.

`conftest.py` starts Chromium, creates a context and page, yields that page to tests, then closes page, context, and browser.

## Prerequisites

- Python 3.10 or later
- pip
- Network access to https://www.saucedemo.com/

## Installation

From the project root (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

`playwright install chromium` downloads the browser used by the tests.

## Environment variables

Copy the example file and adjust if needed:

```powershell
copy .env.example .env
```

```env
BASE_URL=https://www.saucedemo.com/
USERNAME=standard_user
PASSWORD=secret_sauce
```

These are **public SauceDemo demo credentials**. They are fine for this sample app. In a real project, never commit secrets: keep `.env` out of git (this repo gitignores it) and use a secret manager or CI variables instead.

`utils/config.py` loads `.env` with `override=True` so these values win over the Windows `USERNAME` environment variable.

## How to run tests

Run everything (verbose, headless Chromium):

```powershell
pytest
```

or:

```powershell
pytest -v
```

One file:

```powershell
pytest tests/test_login.py -v
```

One test:

```powershell
pytest tests/test_login.py::test_valid_login -v
```

Headed browser:

```powershell
pytest --headed
```

Smoke tests only (`test_valid_login`, `test_add_product_to_cart`, `test_complete_checkout`):

```powershell
pytest -m smoke
```

## Reports

Every `pytest` run writes:

- HTML: `reports/report.html`
- Allure results: `reports/allure-results/`

Open the HTML report in a browser:

```powershell
start reports/report.html
```

Generate and open the Allure report (needs the [Allure commandline](https://allurereport.org/docs/install/)):

```powershell
allure serve reports/allure-results
```

Or write a static Allure site:

```powershell
allure generate reports/allure-results -o reports/allure-report --clean
start reports/allure-report/index.html
```

Install Allure CLI on Windows with Scoop (`scoop install allure`) or Chocolatey (`choco install allure`). Failed tests attach a screenshot to both reports.

## Implemented tests

| Test | What it validates |
|------|-------------------|
| `test_valid_login` | Valid user reaches the Products page |
| `test_invalid_login` | Wrong credentials show an error |
| `test_add_product_to_cart` | Adding an item updates the cart badge |
| `test_product_is_present_in_cart` | The selected product appears in the cart |
| `test_complete_checkout` | Full checkout, overview summary, order confirmation |
| `test_checkout_requires_customer_information` | Checkout cannot continue with empty customer fields |

## Suggested next steps

Not included in this demo, but useful later:

- GitHub Actions CI
- Parallel runs (`pytest-xdist`)
- Firefox / WebKit in addition to Chromium
- Screenshot and video on failure
- API + UI hybrid checks
- A dedicated test-data layer (JSON/YAML) for products and users
