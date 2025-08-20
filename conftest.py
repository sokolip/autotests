import os
import pytest
from pages.login_page import LoginPage
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
AUTH_STATE_FILE = "auth.json"

@pytest.fixture(scope="session")
def auth_storage_state_file(browser):
    context = browser.new_context()
    page = context.new_page()

    login = LoginPage(page)
    login.open_login_page()
    login.login_with_username()
    login.skip_2fa()
    login.skip_greeting_message()
    login.main_page_is_opened()

    context.storage_state(path=AUTH_STATE_FILE)
    context.close()
    return AUTH_STATE_FILE


@pytest.fixture
def authorized_page(browser, auth_storage_state_file):
    context = browser.new_context(storage_state=auth_storage_state_file)
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    context.close()
