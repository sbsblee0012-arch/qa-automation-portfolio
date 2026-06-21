# QA 자동화 테스트 포트폴리오

[![QA 자동화 테스트](https://github.com/sbsblee0012-arch/qa-automation-portfolio/actions/workflows/test.yml/badge.svg)](https://github.com/sbsblee0012-arch/qa-automation-portfolio/actions/workflows/test.yml)

Playwright와 pytest를 활용한 웹 UI · API 자동화 테스트 프로젝트입니다.
saucedemo.com 대상 UI End-to-End 자동화와 jsonplaceholder 대상 API 테스트를 GitHub Actions CI에서 자동 실행합니다.

## 🛠 사용 기술

- Python 3.13
- Playwright (UI 자동화)
- pytest · pytest-html (테스트 실행 · 리포트)
- requests (API 테스트)
- python-dotenv (환경변수 관리)
- GitHub Actions (CI/CD)

## 📁 프로젝트 구조

\`\`\`
qa-automation-portfolio/
├── .github/workflows/
│   └── test.yml            # CI 워크플로 (push·PR 시 자동 실행)
├── pages/                  # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py       # 로그인 (성공/실패/빈값)
│   ├── test_cart.py        # 장바구니
│   ├── test_e2e.py         # 전체 구매 흐름 E2E
│   └── test_api.py         # API (조회/생성/삭제)
├── conftest.py
├── requirements.txt
└── README.md
\`\`\`

## ✅ 테스트 시나리오

### UI 자동화 (Playwright)
- 로그인 성공 / 실패 / 빈값 검증
- 장바구니 추가 및 페이지 이동
- 전체 구매 흐름 E2E (로그인 → 상품 선택 → 장바구니 → 결제 완료)

### API 자동화 (requests)
- 유저 조회 (정상 / 음수 케이스)
- parametrize 기반 반복 테스트
- 게시글 생성 (POST) / 삭제 (DELETE)

## ▶️ 실행 방법

\`\`\`bash
# 1. 의존성 설치
pip install -r requirements.txt
playwright install

# 2. 전체 테스트 실행
pytest tests/ -v

# 3. HTML 리포트 생성
pytest tests/ -v --html=report.html --self-contained-html
\`\`\`

> 로컬에서는 브라우저 화면이 보이는 모드로, CI에서는 화면 없는(headless) 모드로 자동 전환됩니다. \`os.getenv("CI")\`로 실행 환경을 판별합니다.

## 🔄 CI/CD (GitHub Actions)

- \`main\` 브랜치 push 및 Pull Request 시 UI · API 테스트 전체 자동 실행
- Actions 탭에서 수동 실행(workflow_dispatch) 지원
- 실행 후 HTML 리포트를 아티팩트로 업로드 (실패 시에도 업로드)

## 환경변수

로컬 실행 시 `.env.example`을 참고해 `.env` 파일을 생성하세요.

```
BASE_URL=https://jsonplaceholder.typicode.com
```
