#возможно делать эти проверки только на проде до момента редиректа
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
import allure
import re

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


class BalancePage(BasePage):
    @allure.step("Открытие вкладки Баланс")
    def open(self):
        self.page.goto(f"{BASE_URL}/me/balance")

    @allure.step("Проверка UI элементов вкладки Баланс")
    def check_balance_page_ui(self):
        expect(self.page.get_by_text("Мой баланс, BL")).to_be_visible()
        expect(self.page.get_by_text("Лимит, BL")).to_be_visible()
        expect(self.page.get_by_text("Всего получено, BL")).to_be_visible()
        expect(self.page.get_by_text("Списано, BL")).to_be_visible()
        expect(self.page.locator("input.Switch-Input")).to_be_checked()
        expect(self.page.get_by_text("Дополнительно спишем 1 BL")).to_be_visible()

    @allure.step("Проверка тоггла uLime")
    def check_toggle_ulime(self):
        toggle = self.page.get_by_text("Показывать uLime")
        toggle.click()
        bitlime_label = self.page.locator("xpath=//label[input[@value='balanceChoiceGroup-Bitlime']]//span[text()='Bitlime']")
        expect(bitlime_label).not_to_be_visible(timeout=5000)
        toggle.click()
        expect(bitlime_label).to_be_visible(timeout=5000)

    def add_currency_count(self, amount: str):
        field = self.page.get_by_placeholder("Введите необходимое количество")
        field.click()
        field.fill(amount)
        expect(field).to_have_value(amount)

    def _top_up(self, currency_testid: str, method_testid: str, amount: str):
        self.page.get_by_test_id(currency_testid).click()
        self.page.get_by_test_id(method_testid).click()
        self.add_currency_count(amount)
        self.page.get_by_role("button", name="Пополнить баланс").click()

    @allure.step("Пополнение Lime-BTC")
    def top_up_lime_btc(self, amount: str):
        self._top_up(currency_testid="currency-lime", method_testid="payment-method-btc", amount=amount)
        #для тестового контура
        self.page.get_by_role("button", name="Закрыть").click()

    @allure.step("Пополнение Lime-RUB")
    def top_up_lime_rub(self, amount: str):
        parent = self.page
        with parent.expect_popup() as popup_info:
            self._top_up(currency_testid="currency-lime ads", method_testid="payment-method-rub", amount=amount)
        new_tab = popup_info.value
        new_tab.wait_for_load_state("domcontentloaded")
        field = new_tab.locator("input.TextField-Input")
        expect(field).to_be_visible()
        expect(field).to_have_value(str(amount))
        new_tab.close()
        parent.bring_to_front()

    @allure.step("Пополнение Lime-USDT")
    def top_up_lime_usdt(self, amount: str):
        self._top_up(currency_testid="currency-lime", method_testid="payment-method-usdt", amount=amount)

    @allure.step("Пополнение Lime-uLime")
    def top_up_lime_ulime(self, amount: str):
        self._top_up(currency_testid="currency-lime", method_testid="payment-method-uLime", amount=amount)

    @allure.step("Пополнение Lime Ads-USDT")
    def top_up_limeads_usdt(self, amount: str):
        self._top_up(currency_testid="currency-lime ads", method_testid="payment-method-usdt", amount=amount)

    @allure.step("Пополнение Lime Ads-Lime")
    def top_up_limeads_lime(self, amount: str):
        self._top_up(currency_testid="currency-lime ads", method_testid="payment-method-lime", amount=amount)

    #Модалка подтверждения перевода
    def assert_transfer_confirm_modal(self, username: str, amount: str | int):
        modal = self.page.locator("#scrollableTargetModal")
        expect(modal).to_be_visible(timeout=5000)

        expect(modal.get_by_text("Подтвердите перевод пользователю")).to_be_visible()

        expect(
            modal.get_by_text(re.compile(rf"Имя пользователя\s*:\s*{re.escape(str(username))}"))
        ).to_be_visible()

        expect(
            modal.get_by_text(re.compile(rf"Сумма перевода\s*:\s*{re.escape(str(amount))}"))
        ).to_be_visible()

        confirm_btn = modal.get_by_role("button", name="Подтвердить перевод")
        cancel_btn  = modal.get_by_role("button", name="Отменить перевод")
        expect(confirm_btn).to_be_visible()
        expect(cancel_btn).to_be_visible()

        close_btn = modal.locator("[role='button']").filter(has=modal.locator(".Close")).first
        expect(close_btn).to_be_visible()

        return modal, confirm_btn, cancel_btn, close_btn

    @allure.step("Перевод пользователю Lime по никнейму")
    def transfer_lime_by_nickname(self, section_title: str, option_text: str, payee_username: str, amount: str):
        self.select_dropdown_option(section_title=section_title, option_text=option_text)
        self.page.get_by_test_id("lime").click()
        self.page.locator("input[name='credentials']").fill(payee_username)
        self.page.locator("input[name='amount']").fill(amount)
        self.page.get_by_role("button", name="Перевести пользователю").click()
        return self.assert_transfer_confirm_modal(username=payee_username, amount=amount)
