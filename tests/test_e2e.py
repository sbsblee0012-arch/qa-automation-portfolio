import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage

def test_전체_구매_흐름():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. 로그인
        login = LoginPage(page)
        login.open()
        login.login("standard_user", "secret_sauce")

        # 2. 상품 선택 & 장바구니
        inventory = InventoryPage(page)
        inventory.click_first_item()
        inventory.add_to_cart()
        assert inventory.get_cart_count() == "1"

        # 3. 장바구니 이동
        inventory.go_to_cart()
        assert "cart" in page.url

        # 4. 결제
        page.click("[data-test='checkout']")
        checkout = CheckoutPage(page)
        checkout.enter_info("길동", "김", "12345")
        checkout.continue_checkout()
        checkout.finish()
        assert checkout.is_complete()

        browser.close()