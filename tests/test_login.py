from pages.login_page import LoginPage


def test_login_page(page):
    login = LoginPage(page)
    login.open_login_page()
    login.check_ui_elements()
    login.login_with_email()
    login.skip_2fa()
    login.skip_greeting_message()
    login.main_page_is_opened()

    print("Успешный логин - тестовый пользователь попал в личный кабинет")



