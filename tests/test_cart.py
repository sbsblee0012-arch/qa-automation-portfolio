import os
from playwright.sync_api import sync_playwright
import pytest

@pytest.fixture
def logged_in_page():
    """로그인된 상태의 페이지를 준비해두는 fixture"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=os.getenv("CI") == "true")
        page = browser.new_page()

        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        yield page  # 로그인된 페이지를 테스트에 넘겨줌

        browser.close()


def test_상품_장바구니_추가(logged_in_page):
    page = logged_in_page

    # 첫 번째 상품 담기
    page.click(".btn_primary")

    # 장바구니 숫자가 1로 바뀌었는지 확인
    badge = page.locator(".shopping_cart_badge")
    assert badge.inner_text() == "1"
    print("✅ 장바구니 추가 성공!")


def test_장바구니_페이지_이동(logged_in_page):
    page = logged_in_page

    # 상품 담고
    page.click(".btn_primary")

    # 장바구니 아이콘 클릭
    page.click(".shopping_cart_link")

    # 장바구니 페이지로 이동했는지 확인
    assert "cart" in page.url
    print("✅ 장바구니 페이지 이동 성공!")