import os
import pytest
from pages.login_page import LoginPage
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def login_and_get_token(page):
    login = LoginPage(page)
    login.login_with_username()
    login.skip_2fa()
    login.skip_greeting_message()
    login.main_page_is_opened()
    cookies = page.context.cookies()
    access_cookie = next((c for c in cookies if c["name"] == "access"), None)
    login = LoginPage(page)
    login.open_login_page()
    assert access_cookie, "Не найден cookie 'access'"
    return access_cookie


@pytest.fixture
def authorized_page(page, login_and_get_token):
    page.context.add_cookies([login_and_get_token])
    page.goto(BASE_URL)
    return page
