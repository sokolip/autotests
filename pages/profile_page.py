from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
import allure
import re

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_USER = os.getenv("TEST_LOGIN")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


class MainPage(BasePage):

    @allure.step("Открываем страницу профайла")
    def open_profile_page(self):
        self.open_page(url=f"{BASE_URL}/profile/me")

    @allure.step("Отображение приветственного сообщения")
    def skip_greeting_message(self):
        try:
            print("Ищем модальное окно...")
            modal = self.page.locator("#scrollableTargetModal")

            # Ждем появления модального окна
            modal.wait_for(state="visible", timeout=3000)
            print("Модальное окно найдено, ищем кнопку закрытия...")

            close_btn = modal.get_by_test_id("baseModalClose")

            # Ждем, что кнопка станет доступной
            close_btn.wait_for(state="visible", timeout=2000)
            print("Кнопка найдена, кликаем...")
            close_btn.click()

            # Ждем, что модальное окно исчезнет
            modal.wait_for(state="hidden", timeout=2000)
            print("Модальное окно закрыто успешно")

        except Exception as e:
            print(f"Ошибка при закрытии модального окна: {e}")
            # Попробуем альтернативные способы закрытия
            try:
                # Возможно, кнопка имеет другой локатор
                self.page.click("button[aria-label='Close']", timeout=1000)
                print("Закрыли через aria-label")
            except:
                try:
                    # Или попробуем ESC
                    self.page.keyboard.press("Escape")
                    print("Закрыли через ESC")
                except:
                    print("Не удалось закрыть модальное окно никаким способом")

    @allure.step("Проверка табов личного кабинета")
    def check_main_page_ui_element(self):
        expect(self.page.get_by_text(TEST_USER)).to_be_visible()
        expect(self.page.get_by_text(TEST_EMAIL)).to_be_visible()
        self.expect_clickable(self.page.locator("//button[text()='Профиль']"))
        self.expect_clickable(self.page.locator("//button[text()='Баланс']"))
        self.expect_clickable(self.page.locator("//button[text()='Статьи']"))
        self.expect_clickable(self.page.locator("//button[text()='Бонусная программа']"))
        self.expect_clickable(self.page.locator("//button[text()='Команда']"))
        self.expect_clickable(self.page.locator("//button[text()='История']"))
        self.expect_clickable(self.page.locator("//button[text()='Заявки']"))
        self.expect_clickable(self.page.locator("//button[text()='Профиль']"))
        self.expect_clickable(self.page.locator("//button[text()='Настройки']"))

    @allure.step("Проверка переключения табов")
    def check_switch_tabs(self):
        tabs = ["Баланс", "Статьи", "Бонусная программа", "Команда", "История", "Заявки", "Профиль", "Настройки"]
        for name in tabs:
            btn = self.page.get_by_role("tab", name=name)
            btn.click()
            expect(btn).to_have_class(re.compile(r".TabsTab_checked.*"), timeout=2000)

    @allure.step("Проверка блока Подписка Plus")
    def check_subscription_plus(self):
        profile_button = self.page.get_by_role("tab", name="Профиль")
        profile_button.click()
        self.click_button("Подробнее")
        self.wait_for_text("Подписка Plus")
        modal = self.page.locator("#scrollableTargetModal")
        modal_box = modal.bounding_box()
        if modal_box:
            self.page.mouse.click(modal_box['x'] - 50, modal_box['y'] + 100)
        self.wait_for_text(TEST_EMAIL)

    @allure.step("Проверка блока с достижениями")
    def get_all_achievements(self):
        self.select_profile_tab()
        self.page.get_by_text("Смотреть все").click()
        self.check_redirect_url_and_go_back(
            expected_redirect_url=f"{BASE_URL}/achievements",
            expected_back_url=f"{BASE_URL}/profile/me"
        )

    @allure.step("Проверка блока с Заданиями")
    def check_tasks(self):
        self.select_profile_tab()
        label = self.page.locator("//label[.//span[text()='Еженедельные']]")
        label.click()
        label = self.page.locator("//label[.//span[text()='Ежедневные']]")
        label.click()


    @allure.step("Проверка блока с Турнирной таблицей")
    def check_tournament_table(self, username: str):
        self.select_profile_tab()
        expect(self.page.locator("#onboard_leagues")).to_be_visible()
        expect(self.page.get_by_text("Турнирная таблица")).to_be_visible()

    @allure.step("Открытие таблицы с историей начислений")
    def open_history_modal(self):
        self.select_profile_tab()
        self.page.wait_for_load_state("networkidle", timeout=5000)
        history_link_locator = self.page.get_by_role("link", name="История начислений")
        history_link_locator.wait_for(state="visible", timeout=10000)
        history_link_locator.scroll_into_if_needed()
        history_link_locator.click()
        expect(self.page.locator("#scrollableTargetModal")).to_be_visible()
        expect(self.page.get_by_text("История начислений")).to_be_visible()
        expect(self.page.get_by_text('Выполнение ежедневного задания: "Ежедневный заход"')).to_be_visible()
        #expect(self.page.locator(".jss883")).to_have_count_above(0)  если не каждый день заходим

    @allure.step("Проверка блока Бонусы")
    def check_bonus_block(self):
        self.select_profile_tab()
        expect(self.page.get_by_text("Бонусы")).to_be_visible()
        expect(self.page.get_by_text("Покупайте опыт")).to_be_visible()
        expect(self.page.get_by_text("Пополняйте баланс")).to_be_visible()
        expect(self.page.get_by_text("Активация партнера")).to_be_visible()
        expect(self.page.get_by_text("Покупка курса")).to_be_visible()
        expect(self.page.get_by_text("Переход на новый уровень бонусной программы")).to_be_visible()

    @allure.step("Проверка блока Мои курсы")
    def check_my_courses(self):
        self.select_profile_tab()
        expect(self.page.locator("#onboard_courses")).to_be_visible()

    @allure.step("Проверка партнерской ссылки")
    def check_partner_link_button(self) -> None:
        partner_link_button = self.page.get_by_role("button", name="Скопировать партнёрскую ссылку")
        self.expect_clickable(locator=partner_link_button, description="Скопировать партнерскую ссылку")
        partner_link_button.click()
        self.check_toast(role="status", name="Партнёрская ссылка скопирована")
        