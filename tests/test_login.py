from playwright.sync_api import sync_playwright

def test_로그인_성공():
    with sync_playwright() as p:
        # 브라우저 열기 (headless=False 면 실제로 눈에 보여요)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 연습용 쇼핑몰 사이트 열기
        page.goto("https://www.saucedemo.com")

        # 아이디 입력
        page.fill("#user-name", "standard_user")

        # 비밀번호 입력
        page.fill("#password", "secret_sauce")

        # 로그인 버튼 클릭
        page.click("#login-button")

        # 로그인 후 URL 확인
        assert "inventory" in page.url

        print("✅ 로그인 성공!")
        browser.close()

def test_로그인_실패_틀린비밀번호():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "wrong_password")  # 틀린 비밀번호
        page.click("#login-button")

        # 에러 메시지가 화면에 나타나는지 확인
        error = page.locator("[data-test='error']")
        assert error.is_visible()

        print("✅ 에러 메시지 정상 노출!")
        browser.close()

def test_로그인_실패_빈값():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com")
        page.click("#login-button")  # 아무것도 입력 안 하고 클릭

        error = page.locator("[data-test='error']")
        assert error.is_visible()

        print("✅ 빈값 에러 메시지 정상 노출!")
        browser.close()