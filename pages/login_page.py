from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
from time import sleep
import allure

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_USER = os.getenv("TEST_LOGIN")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_input = self.page.get_by_placeholder("Введите логин")
        self.password_input = self.page.get_by_placeholder("Пароль")
        self.login_button = self.page.get_by_role("button", name="Далее")

    @allure.step("Открываем главную стрраницу")
    def open_login_page(self):
        self.open_page(BASE_URL)
        self.wait_for_page_ready("load")
        self.click_button("Вход / Регистрация")
        self.page.wait_for_url("**/login/callback/")
        self.wait_for_page_ready("load")
        expect(self.page.get_by_text("Вход")).to_be_visible()

    @allure.step("Открытие окна Авторизация")
    def login_with_username(self):
        self.login_input.fill(TEST_USER)
        self.password_input.fill(TEST_PASSWORD)
        self.login_button.click()

    @allure.step("Проверка UI элементов окна авторизации")
    def check_ui_elements(self):
        self.wait_for_page_ready("networkidle")
        assert self.is_visible("//button[@title='google']"), "Кнопка авторизации через Google не отображается"
        self.expect_clickable(self.page.get_by_role("link", name="Регистрация"))
        self.expect_clickable(self.page.get_by_role("link", name="Пользовательского соглашения"))

    @allure.step("Пропускаем 2FA")
    def skip_2fa(self):
        self.click_button(name="Отказаться")

    @allure.step("Отображение приветственного сообщения")
    def skip_greeting_message(self):
        self.page.mouse.click(x=10, y=10)
        # modal = self.page.locator("#scrollableTargetModal")
        # close_btn = modal.get_by_role("button").filter(has=modal.locator(".Close")).first
        # expect(close_btn).to_be_visible()
        # close_btn.close()


    @allure.step("Открытие главной страницы")
    def main_page_is_opened(self):
        try:
            expect(self.page.get_by_text(TEST_EMAIL)).to_be_visible()
            print("Успешный логин - тестовый пользователь попал в личный кабинет")
        except Exception as e:
            print(f"Ошибка при открытии личного кабинета: {e}")
            raise
