from pages.profile_page import MainPage


def test_profile_page_ui_checking(authorized_page):
    profile = MainPage(authorized_page)
    profile.open()
    profile.check_main_page_ui_element()
    profile.check_subscription_plus()
    profile.get_all_achievements()
    profile.check_tasks()
    profile.check_tournament_table(TEST_USER)
    profile.open_history_modal()
    profile.check_bonus_block()
    profile.check_my_courses()
    profile.check_partner_link_button()
