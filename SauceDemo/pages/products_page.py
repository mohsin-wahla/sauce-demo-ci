import re

from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.inventory_list = page.locator("[data-test='inventory-list']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html"))
        expect(self.title).to_have_text("Products")
        expect(self.inventory_list).to_be_visible()

    def add_product_to_cart(self, product_name: str) -> None:
        slug = product_name.lower().replace(" ", "-")
        self.page.locator(f"[data-test='add-to-cart-{slug}']").click()

    def open_cart(self) -> None:
        self.cart_link.click()

    def cart_count(self) -> str:
        return self.cart_badge.inner_text()
