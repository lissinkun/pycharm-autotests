"""HTTP-запросы к ресурсу пользователей."""

import json

import allure


class UsersClient:
    def __init__(self, base_url, session, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.timeout = timeout

    @allure.step("Получить список пользователей")
    def get_users(self):
        return self._request("GET", "/users")

    @allure.step("Получить пользователя с ID {user_id}")
    def get_user(self, user_id):
        return self._request("GET", f"/users/{user_id}")

    @allure.step("Создать пользователя")
    def create_user(self, payload):
        return self._request("POST", "/users", json=payload)

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        allure.attach(
            json.dumps(
                {"method": method, "url": url, "json": kwargs.get("json")},
                ensure_ascii=False,
                indent=2,
            ),
            name="Запрос",
            attachment_type=allure.attachment_type.JSON,
        )
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        allure.attach(
            f"HTTP {response.status_code}\n\n{response.text}",
            name="Ответ API",
            attachment_type=allure.attachment_type.TEXT,
        )
        return response
