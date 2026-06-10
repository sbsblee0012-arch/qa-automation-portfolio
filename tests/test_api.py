from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

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