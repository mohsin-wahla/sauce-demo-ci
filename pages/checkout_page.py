import re

from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator("[data-test='error']")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*checkout-step-one"))
        expect(self.title).to_have_text("Checkout: Your Information")

    def fill_customer_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_overview(self) -> None:
        self.continue_button.click()

    def expect_error_visible(self) -> None:
        expect(self.error_message).to_be_visible()

    def error_text(self) -> str:
        return self.error_message.inner_text()
