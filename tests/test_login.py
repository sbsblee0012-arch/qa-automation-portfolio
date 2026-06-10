import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


def test_로그인_성공(page):
    login = LoginPage(page)
    login.open()
    login.login("standard_user", "secret_sauce")

    assert "inventory" in page.url
    print("✅ 로그인 성공!")


@pytest.mark.parametrize("아이디, 비밀번호, 기대에러", [
    ("standard_user", "wrong_password", "Username and password do not match"),
    ("", "", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("invalid_user", "secret_sauce", "Username and password do not match"),
])
def test_로그인_실패(page, 아이디, 비밀번호, 기대에러):
    login = LoginPage(page)
    login.open()
    login.login(아이디, 비밀번호)

    error = page.locator("[data-test='error']")
    assert error.is_visible()
    assert 기대에러 in error.inner_text()
    print(f"✅ 에러 확인: {기대에러}")