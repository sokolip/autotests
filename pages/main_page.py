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


class MainPage(BasePage):
    @allure.step("Проверка табов личного кабинета")
    def check_main_page_ui_element(self):
        expect(self.page.get_by_text(TEST_USER)).to_be_visible()
        expect(self.page.get_by_text(TEST_EMAIL)).to_be_visible()
        self.expect_clickable(locator="//button[text()='Профиль']").click()
        self.expect_clickable(locator="//button[text()='Баланс']").click()
        self.expect_clickable(locator="//button[text()='Статьи']").click()
        self.expect_clickable(locator="//button[text()='Бонусная программа']").click()
        self.expect_clickable(locator="//button[text()='Команда']").click()
        self.expect_clickable(locator="//button[text()='История']").click()
        self.expect_clickable(locator="//button[text()='Заявки']").click()
        self.expect_clickable(locator="//button[text()='Профиль']").click()
        self.expect_clickable(locator="//button[text()='Настройки']").click()

    @allure.step("Проверка блока Подписка Plus")
    def check_subscription_plus(self):
        self.click_button("Профиль")
        self.click_button("Подробнее")
        self.wait_for_text("Подписка Plus")
        self.page.mouse.click(x=10, y=10)

    @allure.step("Проверка блока с достижениями")
    def get_all_achievements(self):
        self.page.get_by_text("Смотреть все").click()
        self.check_redirect_url_and_go_back("**/achievements")
        self.wait_for_url("**/me")

    @allure.step("Проверка блока с Заданиями")
    def check_tasks(self):
        self.expect_clickable(locator="//button[text()='Еженедельные']").click()
        self.expect_clickable(locator="//button[text()='Ежедневные']").click()

    @allure.step("Проверка блока с Турнирной таблицей")
    def check_tournament_table(self, username: str):
        expect(self.page.locator("#onbboard_leagues")).to_be_visible()
        expect(self.page.get_by_text("Турнирная таблица")).to_be_visible()
        expect(self.page.get_by_text(username)).to_be_visible()

    @allure.step("Открытие таблицы с историей начислений")
    def open_history_modal(self):
        self.page.get_by_text("История начислений").click()
        expect(self.page.locator("#scrollableTargetModal")).to_be_visible()
        expect(self.page.get_by_text("История начислений")).to_be_visible()
        expect(self.page.get_by_text('Выполнение ежедневного задания: "Ежедневный заход"')).to_be_visible()
        #expect(self.page.locator(".jss883")).to_have_count_above(0)  если не каждый день заходим

    @allure.step("Проверка блока Бонусы")
    def check_bonus_block(self):
        self.page.get_by_text("Бонусы").to_be_visible()
        self.page.get_by_text("Покупайте опыт").to_be_visible()
        self.page.get_by_text("Пополняйте баланс").to_be_visible()
        self.page.get_by_text("Активация партнера").to_be_visible()
        self.page.get_by_text("Покупка курса").to_be_visible()
        self.page.get_by_text("Переход на новый уровень бонусной программы").to_be_visible()

    @allure.step("Проверка блока Мои курсы")
    def check_my_courses(self):
        expect(self.page.locator("#onboard_courses")).to_be_visible()





















        







