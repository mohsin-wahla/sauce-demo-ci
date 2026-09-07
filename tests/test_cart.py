import pytest

from utils.config import DEFAULT_PRODUCT


@pytest.mark.smoke
def test_add_product_to_cart(products_page) -> None:
    products_page.add_product_to_cart(DEFAULT_PRODUCT)
    assert products_page.cart_count() == "1"


def test_product_is_present_in_cart(products_page, cart_page) -> None:
    products_page.add_product_to_cart(DEFAULT_PRODUCT)
    products_page.open_cart()
    cart_page.expect_loaded()
    cart_page.expect_product_present(DEFAULT_PRODUCT)
