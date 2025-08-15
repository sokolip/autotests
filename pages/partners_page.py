from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
from time import sleep
import allure

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

class PartnersPage(BasePage):

    @allure.step("Открытие вкладки Бонусная программа")
    def open(self):
        self.page.goto(f"{BASE_URL}/me/partners")






