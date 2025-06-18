import requests
import allure
import json
import logging

class ApiClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"
    REGISTER_PATH = "/auth/register"
    LOGIN_PATH = "/auth/login"
    USER_PATH = "/auth/user"
    ORDERS_PATH = "/orders"
    INGREDIENTS_PATH = "/ingredients"

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

    @allure.step("Создание пользователя")
    def create_user(self, user_data):
        endpoint = f"{self.BASE_URL}{self.REGISTER_PATH}"
        response = requests.post(
            endpoint,
            data=json.dumps(user_data),
            headers=self.headers
        )
        self.logger.info(f"Запрос создания пользователя: {user_data}")
        self.logger.info(f"Ответ: {response.status_code}, {response.text}")
        return response

    @allure.step("Логин пользователя")
    def login_user(self, credentials):
        endpoint = f"{self.BASE_URL}{self.LOGIN_PATH}"
        response = requests.post(
            endpoint,
            data=json.dumps(credentials),
            headers=self.headers
        )
        self.logger.info(f"Запрос логина: {credentials}")
        self.logger.info(f"Ответ: {response.status_code}, {response.text}")
        return response

    @allure.step("Обновление данных пользователя")
    def update_user(self, user_data, token=None):
        endpoint = f"{self.BASE_URL}{self.USER_PATH}"
        headers = self.headers.copy()

        if token:
            if token.startswith("Bearer "):
                token_value = token.split("Bearer ")[1]
                headers["Authorization"] = f"Bearer {token_value}"
            else:
                headers["Authorization"] = f"Bearer {token}"

        response = requests.patch(
            endpoint,
            json=user_data,
            headers=headers
        )
        self.logger.info(f"Запрос обновления пользователя: {user_data}")
        self.logger.info(f"Ответ: {response.status_code}, {response.text}")
        return response

    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        endpoint = f"{self.BASE_URL}{self.ORDERS_PATH}"
        headers = self.headers.copy()

        if token:
            headers["Authorization"] = token

        response = requests.post(
            endpoint,
            data=json.dumps({"ingredients": ingredients}),
            headers=headers
        )
        self.logger.info(f"Запрос создания заказа: {ingredients}")
        self.logger.info(f"Ответ: {response.status_code}, {response.text}")
        return response

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, token=None):
        endpoint = f"{self.BASE_URL}{self.ORDERS_PATH}"
        headers = self.headers.copy()

        if token:
            headers["Authorization"] = token

        response = requests.get(
            endpoint,
            headers=headers
        )
        self.logger.info("Запрос получения заказов пользователя")
        self.logger.info(f"Ответ: {response.status_code}, {response.text}")
        return response

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        endpoint = f"{self.BASE_URL}{self.INGREDIENTS_PATH}"
        response = requests.get(endpoint, headers=self.headers)
        self.logger.info("Запрос получения списка ингредиентов")
        self.logger.info(f"Ответ: {response.status_code}")
        return response