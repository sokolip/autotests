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

    def expect_clickable(self, locator, description="элемент"):
        try:
            expect(locator).to_be_visible()
            expect(locator).to_be_enabled()
        except Exception as e:
            print(f"[FAIL] {description} не кликабелен: {e}")

    def wait_for_page_ready(self, state="load", timeout=10000):
        self.page.wait_for_load_state(state=state, timeout=timeout)

    def check_redirect_url_and_go_back(self, expected_url_path: str):
        expect(self.page).to_have_url(expected_url_path)
        response = self.page.go_back()
        assert response is not None, "Не удалось вернуться на предыдущую страницу"

    def select_dropdown_option(self, section_title: str, option_text: str, *, timeout=5000):
        section = self.page.locator(f"xpath=//div[.//div[normalize-space(text())='{section_title}']]")
        expect(section).to_be_visible(timeout=timeout)
        trigger = section.locator("button:has(.IconArrowDown)")
        expect(trigger).to_be_visible(timeout=timeout)
        trigger.click()
        listbox = self.page.locator("[role='listbox'], [role='menu'], .Menu, .Dropdown, .Select-Menu").first
        expect(listbox).to_be_visible(timeout=timeout)
        option = listbox.get_by_role("option", name=option_text)
        if option.count() == 0:
            option = listbox.locator(f"text={option_text}")
        expect(option).to_be_visible(timeout=timeout)
        option.click()
        expect(listbox).not_to_be_visible()


    #для всех вкладок
    def check_toast(self, role: str, name: str, appear_timeout: int = 3000, disappear_timeout: int = 8000):
        toast = self.page.get_by_role(role=role, name=name).first
        expect(toast).to_be_visible(timeout=appear_timeout)
        expect(toast).to_be_visible(timeout=disappear_timeout)

    def check_partner_link_button(self) -> None:
        partner_link_button = self.page.get_by_role("button", name="Скопировать партнёрскую ссылку")
        self.expect_clickable(locator=partner_link_button, description="Скопировать партнерскую ссылку")
        partner_link_button.click()
        self.check_toast(role="status", name="Партнёрская ссылка скопирована")
