import pytest

from utils.config import DEFAULT_PRODUCT


@pytest.mark.smoke
def test_complete_checkout(
    products_page,
    cart_page,
    checkout_page,
    checkout_overview_page,
) -> None:
    products_page.add_product_to_cart(DEFAULT_PRODUCT)
    products_page.open_cart()
    cart_page.expect_loaded()
    cart_page.expect_product_present(DEFAULT_PRODUCT)

    cart_page.checkout()
    checkout_page.expect_loaded()
    checkout_page.fill_customer_information("Jane", "Doe", "12345")
    checkout_page.continue_to_overview()

    checkout_overview_page.expect_loaded()
    checkout_overview_page.expect_product_present(DEFAULT_PRODUCT)
    checkout_overview_page.expect_order_summary_visible()

    checkout_overview_page.finish()
    checkout_overview_page.expect_order_complete()


def test_checkout_requires_customer_information(
    products_page,
    cart_page,
    checkout_page,
) -> None:
    products_page.add_product_to_cart(DEFAULT_PRODUCT)
    products_page.open_cart()
    cart_page.checkout()
    checkout_page.expect_loaded()
    checkout_page.continue_to_overview()
    checkout_page.expect_error_visible()
    assert "First Name is required" in checkout_page.error_text()
