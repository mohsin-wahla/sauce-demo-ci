from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def goto(self, base_url: str) -> None:
        self.page.goto(base_url)

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_error_visible(self) -> None:
        expect(self.error_message).to_be_visible()

    def error_text(self) -> str:
        return self.error_message.inner_text()
