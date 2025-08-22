#возможно делать эти проверки только на проде до момента редиректа
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
import allure
import re

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
BTC_PAY_TEST_URL = os.getenv("BTC_PAY_TEST_URL")
RUB_PAY_TEST_URL = os.getenv("RUB_PAY_TEST_URL")

class BalancePage(BasePage):
    @allure.step("Открытие вкладки Баланс")
    def open_balance_tab(self, url=f"{BASE_URL}/profile/me"):
        self.open_page(url=url)
        self.page.get_by_role("tab", name="Баланс").click()

    @allure.step("Проверка UI элементов вкладки Баланс")
    def check_balance_page_ui(self):
        expect(self.page.get_by_text("Мой баланс, BL")).to_be_visible()
        expect(self.page.get_by_text("Лимит, BL")).to_be_visible()
        expect(self.page.get_by_text("Всего получено, BL")).to_be_visible()
        expect(self.page.get_by_text("Списано, BL")).to_be_visible()
        expect(self.page.locator("input.Switch-Input")).to_be_checked()
        expect(self.page.get_by_text("Дополнительно спишем 1 BL")).to_be_visible()
        radio_button_bitlime_locator = self.page.get_by_role("radio", name="Bitlime")
        expect(radio_button_bitlime_locator.first).to_be_checked()
        #нужно добавить testid
        # radio_button_ulime_locator = self.page.get_by_role("radio", name="uLime")
        # radio_button_ulime_locator.first.click()
        # expect(radio_button_ulime_locator.first).to_be_checked()
        # radio_button_bitlime_locator.first.click()


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
        self.page.locator("body").click()
        self.page.get_by_role("button", name="Пополнить баланс").click()

    @allure.step("Пополнение Lime-BTC")
    def top_up_lime_btc(self, amount: str):
        parent = self.page
        with parent.expect_popup() as popup_info:
            self._top_up(currency_testid="currency-lime", method_testid="payment-method-btc", amount=amount)
        new_tab = popup_info.value
        new_tab.wait_for_url(f"{BTC_PAY_TEST_URL}/*")
        shop_name_locator = new_tab.locator("xpath=//*[@class='store-name' and text()='academy-test']")
        expect(shop_name_locator).to_be_visible()
        expect(new_tab.locator("#AmountDue")).to_have_text("0.00101000 BTC")
        expect(new_tab.locator("xpath=//a[@id='PayInWallet']")).to_be_visible()
        new_tab.close()
        parent.bring_to_front()

    @allure.step("Пополнение Lime-RUB")
    def top_up_lime_rub(self, amount: str):
        parent = self.page
        with parent.expect_popup() as popup_info:
            self._top_up(currency_testid="currency-lime", method_testid="payment-method-rub", amount=amount)
        new_tab = popup_info.value
        new_tab.wait_for_url(f"{RUB_PAY_TEST_URL}*")
        amount_locator = new_tab.locator("input.TextField-Input[name='amount']")
        actual_amount = amount_locator.input_value()
        expect_amount ="100.00"
        assert actual_amount == expect_amount, f"[FAIL] Поле с суммой должно содержать {expect_amount}, но содержит {actual_amount}"
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

    @allure.step("Проверка кнопки Скачать CSV")
    def check_download_csv_buttom(self):
        download_csv_button = self.page.get_by_role("button", name="Скачать CSV")
        self.expect_clickable(locator=download_csv_button, description="Кнопка скачать CSV")

    @allure.step("Проверка кнопки Искать")
    def check_search_button(self):
        search_button = self.page.get_by_role("button", name="Искать")
        self.expect_clickable(locator=search_button, description="Кнопка Искать")
