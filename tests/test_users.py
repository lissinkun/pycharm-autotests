"""Первые независимые тесты API пользователей JSONPlaceholder."""

import allure
import pytest


@allure.feature("API пользователей")
@allure.title("Получение списка пользователей")
def test_get_users(users_client):
    response = users_client.get_users()

    with allure.step("Проверить статус 200 и поля пользователей"):
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0
        for user in users:
            assert {"id", "name", "username", "email"} <= user.keys()
            assert isinstance(user["id"], int)


@allure.feature("API пользователей")
@allure.title("Получение пользователя с ID {user_id}")
@pytest.mark.parametrize(
    "user_id, expected_name, expected_email",
    [
        (1, "Leanne Graham", "Sincere@april.biz"),
        (2, "Ervin Howell", "Shanna@melissa.tv"),
        (3, "Clementine Bauch", "Nathan@yesenia.net"),
    ],
    ids=["user-1", "user-2", "user-3"],
)
def test_get_existing_user(users_client, user_id, expected_name, expected_email):
    response = users_client.get_user(user_id)

    with allure.step("Проверить статус 200 и данные пользователя"):
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == user_id
        assert user["name"] == expected_name
        assert user["email"] == expected_email


@allure.feature("API пользователей")
@allure.title("Запрос отсутствующего пользователя с ID {user_id}")
@pytest.mark.parametrize("user_id", [0, 999999], ids=["zero", "large-id"])
def test_get_nonexistent_user(users_client, user_id):
    response = users_client.get_user(user_id)

    with allure.step("Проверить статус 404 и пустой объект"):
        assert response.status_code == 404
        assert response.json() == {}


@allure.feature("API пользователей")
@allure.title("Создание пользователя")
def test_create_user(users_client):
    payload = {
        "name": "QA Student",
        "username": "qa_student",
        "email": "qa.student@example.com",
    }

    response = users_client.create_user(payload)

    with allure.step("Проверить статус 201, ID и переданные поля"):
        assert response.status_code == 201
        user = response.json()
        assert isinstance(user["id"], int)
        assert user["id"] > 0
        for field, expected_value in payload.items():
            assert user[field] == expected_value
