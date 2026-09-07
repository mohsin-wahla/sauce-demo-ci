import re

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.cart_list = page.locator("[data-test='cart-list']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.item_names = page.locator("[data-test='inventory-item-name']")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/cart\.html"))
        expect(self.title).to_have_text("Your Cart")
        expect(self.cart_list).to_be_visible()

    def expect_product_present(self, product_name: str) -> None:
        expect(self.item_names.filter(has_text=product_name)).to_be_visible()

    def checkout(self) -> None:
        self.checkout_button.click()
