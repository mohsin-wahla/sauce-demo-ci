import re

from playwright.sync_api import Page, expect


class CheckoutOverviewPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.subtotal = page.locator("[data-test='subtotal-label']")
        self.tax = page.locator("[data-test='tax-label']")
        self.total = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")
        self.complete_header = page.locator("[data-test='complete-header']")
        self.complete_text = page.locator("[data-test='complete-text']")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*checkout-step-two"))
        expect(self.title).to_have_text("Checkout: Overview")

    def expect_product_present(self, product_name: str) -> None:
        expect(self.item_names.filter(has_text=product_name)).to_be_visible()

    def expect_order_summary_visible(self) -> None:
        expect(self.subtotal).to_be_visible()
        expect(self.tax).to_be_visible()
        expect(self.total).to_be_visible()

    def finish(self) -> None:
        self.finish_button.click()

    def expect_order_complete(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*checkout-complete"))
        expect(self.complete_header).to_have_text("Thank you for your order!")
        expect(self.complete_text).to_be_visible()
