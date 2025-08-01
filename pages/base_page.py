from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page):
        self.page = page

    def open_page(self, url):
        self.page.goto(url)

    def wait_for_url(self, url_part: str, timeout=5000):
        self.page.wait_for_url(f"**{url_part}**", timeout=5000)

    def wait_for_text(self, text: str, timeout=5000):
        self.page.get_by_text(text).wait_for(timeout=5000)

    def fill_input(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def click_button(self, name: str):
        button = self.page.get_by_role("button", name=name)
        expect(button).to_be_visible()
        button.click()

    def expect_clickable(self, locator):
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()

    def wait_for_page_ready(self, state="load", timeout=10000):
        self.page.wait_for_load_state(state=state, timeout=timeout)

