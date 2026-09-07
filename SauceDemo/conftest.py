from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, sync_playwright
from pytest_html import extras

from pages.cart_page import CartPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import BASE_URL, PASSWORD, USERNAME


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Chromium in headed mode instead of headless.",
    )


def pytest_configure(config: pytest.Config) -> None:
    Path("reports/allure-results").mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    screenshot = page.screenshot()
    allure.attach(
        screenshot,
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    report.extras = getattr(report, "extras", []) + [
        extras.png(screenshot, "failure-screenshot")
    ]


@pytest.fixture
def page(request: pytest.FixtureRequest):
    headed = request.config.getoption("--headed")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed)
        context = browser.new_context()
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.goto(BASE_URL)
    return login


@pytest.fixture
def products_page(login_page: LoginPage, page: Page) -> ProductsPage:
    """Open SauceDemo and log in with the configured valid user."""
    login_page.login(USERNAME, PASSWORD)
    products = ProductsPage(page)
    products.expect_loaded()
    return products


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)
