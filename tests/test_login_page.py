from pages.login_page import LoginPage
from datetime import sleep


def test_login_page(page):
    login = LoginPage(page)
    login.open_login_page()
    login.check_ui_elements()
    login.login_with_username()
    login.skip_2fa()
    login.skip_greeting_message()
