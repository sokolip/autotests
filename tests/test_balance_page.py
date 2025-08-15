from pages.balance_page import BalancePage

amount = "100"
section_title = "Перевод пользователю"
option_text = "пользователю"
payee_username = "maitest"



def test_balance_tab(authorized_page):
    balance_page = BalancePage(authorized_page)
    balance_page.open()
    balance_page.check_balance_elements()
    balance_page.check_toggle_ulime()
    balance_page.top_up_lime_btc(amount=amount)
    balance_page.top_up_lime_rub(amount=amount)
    balance_page.top_up_lime_usdt(amount=amount)
    balance_page.top_up_limeads_usdt(amount=amount)
    balance_page.top_up_limeads_lime(amount=amount)
    balance_page.transfer_lime_by_nickname()