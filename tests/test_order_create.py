import pytest
import allure
import random

@allure.feature('Создание заказа')
class TestOrderCreate:

    @allure.story('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_auth(self, api_client, registered_user, ingredient_ids):
        _, token = registered_user
        selected_ingredients = random.sample(ingredient_ids, k=3)

        response = api_client.create_order(selected_ingredients, token)

        assert response.status_code == 200, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is True, "Ответ не содержит success:true"
        assert 'order' in data, "Нет данных заказа в ответе"

    @allure.story('Создание заказа без авторизации с ингредиентами')
    def test_create_order_without_auth(self, api_client, ingredient_ids):
        selected_ingredients = random.sample(ingredient_ids, k=3)

        response = api_client.create_order(selected_ingredients)

        assert response.status_code == 200, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is True, "Ответ не содержит success:true"
        assert 'order' in data, "Нет данных заказа в ответе"

    @allure.story('Создание заказа с авторизацией без ингредиентов')
    def test_create_order_without_ingredients(self, api_client, registered_user):
        _, token = registered_user

        response = api_client.create_order([], token)

        assert response.status_code == 400, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is False, "Ответ не содержит success:false"
        assert 'message' in data, "Нет сообщения об ошибке"

    @allure.story('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredients(self, api_client, registered_user):
        _, token = registered_user
        invalid_ingredients = ["invalid-id-1", "invalid-id-2"]

        response = api_client.create_order(invalid_ingredients, token)

        assert response.status_code == 400, "Неверный код ответа"