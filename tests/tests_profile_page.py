from pages.profile_page import MainPage


def test_profile_page_ui_checking(login_as_test_user):
    page = login_as_test_user
    profile = MainPage(page)
    profile.check_main_page_ui_element()
