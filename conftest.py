
import pytest
from pages.login_page import LoginPage

@pytest.fixture()
def login_as_test_user(page):
    login = LoginPage(page)
    login.open_login_page()
    login.login_with_username()
    login.skip_2fa()
    login.skip_greeting_message()
    login.main_page_is_opened()
    return page
