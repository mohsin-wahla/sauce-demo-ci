import pytest

from pages.products_page import ProductsPage
from utils.config import PASSWORD, USERNAME


@pytest.mark.smoke
def test_valid_login(login_page, page) -> None:
    login_page.login(USERNAME, PASSWORD)
    ProductsPage(page).expect_loaded()


def test_invalid_login(login_page) -> None:
    login_page.login("invalid_user", "wrong_password")
    login_page.expect_error_visible()
    assert "Username and password do not match" in login_page.error_text()
