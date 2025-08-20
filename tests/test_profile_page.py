from pages.profile_page import MainPage
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()

TEST_USER = TEST_USER = os.getenv("TEST_LOGIN")
BASE_URL = os.getenv("BASE_URL")

def test_profile_page(authorized_page):
    profile = MainPage(authorized_page)
    profile.open_profile_page()
    profile.skip_greeting_message()
    profile.check_main_page_ui_element()
    profile.check_switch_tabs()
    profile.check_subscription_plus()
    profile.get_all_achievements()
    profile.check_tasks()
    profile.check_tournament_table(TEST_USER)
    profile.open_history_modal()
    profile.check_bonus_block()
    profile.check_my_courses()
    profile.check_partner_link_button()
