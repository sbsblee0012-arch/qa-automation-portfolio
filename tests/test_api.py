from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"

import requests

def test_유저_조회_성공():
    # 1번 유저 정보 요청
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")

    # 상태코드 200인지 확인 (200 = 성공)
    assert response.status_code == 200

    # JSON 응답을 딕셔너리로 변환
    data = response.json()

    # 데이터 확인
    assert data["id"] == 1
    assert data["name"] == "Leanne Graham"
    assert "email" in data

def test_없는_유저_조회():
    response = requests.get("https://jsonplaceholder.typicode.com/users/9999")

    # 없는 유저니까 404가 와야 해요
    assert response.status_code == 404

import pytest

@pytest.mark.parametrize("user_id, 기대이름", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
])
def test_여러_유저_조회(user_id, 기대이름):
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == 기대이름

def test_게시글_생성():
    # 새 게시글 데이터
    new_post = {
        "title": "자동화 테스트 공부중",
        "body": "오늘도 열심히",
        "userId": 1
    }

    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=new_post
    )

    # 생성 성공은 201
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "자동화 테스트 공부중"
    print(f"✅ 생성된 게시글 id: {data['id']}")

def test_게시글_삭제():
    response = requests.delete(f"{BASE_URL}/posts/1")

    # 삭제 성공은 200
    assert response.status_code == 200
    print("✅ 게시글 삭제 성공!")


# ─────────────────────────────────────────────────────────────
# /posts 엔드포인트 테스트 (TC-01 ~ TC-28)
# ─────────────────────────────────────────────────────────────

# TC-01
def test_posts_전체목록_200_및_100개():
    response = requests.get(POSTS_URL)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100


# TC-02
def test_posts_전체목록_항목_필드_존재():
    response = requests.get(POSTS_URL)
    assert response.status_code == 200
    for item in response.json():
        assert "id" in item
        assert "title" in item
        assert "body" in item
        assert "userId" in item


# TC-03
def test_posts_userId_필터_조회():
    response = requests.get(POSTS_URL, params={"userId": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(item["userId"] == 1 for item in data)


# TC-04
def test_posts_존재하지않는_userId_필터_빈배열():
    response = requests.get(POSTS_URL, params={"userId": 0})
    assert response.status_code == 200
    assert response.json() == []


# TC-05 — 실측 확정: userId=abc → 200 + 빈 배열
def test_posts_문자열_userId_필터_응답기록():
    response = requests.get(POSTS_URL, params={"userId": "abc"})
    assert response.status_code == 200
    assert response.json() == []


# TC-06 + TC-07 통합 (동일 엔드포인트 GET /posts/1)
def test_posts_단건_조회_최솟값_id1():
    response = requests.get(f"{POSTS_URL}/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "body" in data
    assert "userId" in data


# TC-08
def test_posts_단건_조회_최댓값_id100():
    response = requests.get(f"{POSTS_URL}/100")
    assert response.status_code == 200
    assert response.json()["id"] == 100


# TC-09 — 실측 확정: /posts/0 → 404 + 빈 객체
def test_posts_단건_조회_id0_응답기록():
    response = requests.get(f"{POSTS_URL}/0")
    assert response.status_code == 404
    assert response.json() == {}


# TC-10
def test_posts_단건_조회_최댓값초과_id101():
    response = requests.get(f"{POSTS_URL}/101")
    assert response.status_code == 404


# TC-11
def test_posts_단건_조회_존재하지않는_id9999():
    response = requests.get(f"{POSTS_URL}/9999")
    assert response.status_code == 404


# TC-12
def test_posts_단건_조회_음수id():
    response = requests.get(f"{POSTS_URL}/-1")
    assert response.status_code == 404


# TC-13
def test_posts_단건_조회_문자열id():
    response = requests.get(f"{POSTS_URL}/abc")
    assert response.status_code == 404


# TC-14
# jsonplaceholder는 실제 저장 없이 항상 id=101을 반환하는 고정 응답
def test_posts_생성_응답id_101_확인():
    payload = {"title": "테스트 제목", "body": "테스트 바디", "userId": 1}
    response = requests.post(POSTS_URL, json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == 101


# TC-15 — title은 test_게시글_생성에 있으므로 body·userId 값·타입만 단언
def test_posts_생성_body_userId_값타입_단언():
    payload = {"title": "타입 테스트", "body": "바디내용", "userId": 2}
    response = requests.post(POSTS_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["body"], str)
    assert data["body"] == payload["body"]
    assert isinstance(data["userId"], int)
    assert data["userId"] == payload["userId"]


# TC-16
def test_posts_생성_body_필드_누락():
    response = requests.post(POSTS_URL, json={"title": "제목", "userId": 1})
    assert response.status_code == 201


# TC-17
def test_posts_생성_userId_필드_누락():
    response = requests.post(POSTS_URL, json={"title": "제목", "body": "내용"})
    assert response.status_code == 201


# TC-18 — 빈 객체 전송: 가짜 API가 입력 검증 없이 201을 반환하는 특성 검증
def test_posts_생성_빈객체_전송():
    response = requests.post(POSTS_URL, json={})
    assert response.status_code == 201


# TC-19
def test_posts_생성_추가필드_포함():
    payload = {"title": "제목", "body": "내용", "userId": 1, "extra": "x"}
    response = requests.post(POSTS_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    print(f"\n[TC-19] extra 필드 응답 포함 여부: {'extra' in data}")


# TC-20
def test_posts_생성_응답_값타입_전체_검증():
    payload = {"title": "타입검증", "body": "바디", "userId": 3}
    response = requests.post(POSTS_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)
    assert isinstance(data["userId"], int)


# TC-21 — status 200은 test_게시글_삭제에 있으므로 body {} 단언만 추가
def test_posts_삭제_응답body_빈객체():
    response = requests.delete(f"{POSTS_URL}/1")
    assert response.status_code == 200
    assert response.json() == {}


# TC-22
def test_posts_삭제_최댓값_id100():
    response = requests.delete(f"{POSTS_URL}/100")
    assert response.status_code == 200


# TC-23
def test_posts_삭제_존재하지않는_id9999():
    response = requests.delete(f"{POSTS_URL}/9999")
    assert response.status_code == 200


# TC-24
def test_posts_삭제_음수id():
    response = requests.delete(f"{POSTS_URL}/-1")
    assert response.status_code == 200


# TC-25
def test_posts_목록_content_type():
    response = requests.get(POSTS_URL)
    assert "application/json" in response.headers.get("Content-Type", "")


# TC-26
def test_posts_단건_content_type():
    response = requests.get(f"{POSTS_URL}/1")
    assert "application/json" in response.headers.get("Content-Type", "")


# TC-27
def test_posts_생성_content_type():
    response = requests.post(POSTS_URL, json={"title": "t", "body": "b", "userId": 1})
    assert "application/json" in response.headers.get("Content-Type", "")


# TC-28
def test_posts_삭제_content_type():
    response = requests.delete(f"{POSTS_URL}/1")
    assert "application/json" in response.headers.get("Content-Type", "")