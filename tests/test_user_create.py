import pytest
import allure
from helpers.data_generator import generate_user_data

@allure.feature('Создание пользователя')
class TestUserCreate:

    @allure.story('Создание уникального пользователя')
    def test_create_unique_user(self, api_client, user_data):
        response = api_client.create_user(user_data)

        assert response.status_code == 200, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is True, "Ответ не содержит success:true"
        assert 'accessToken' in data, "Не получен токен доступа"
        assert 'user' in data, "Нет данных пользователя в ответе"
        assert data['user']['email'] == user_data['email'], "Email не совпадает"
        assert data['user']['name'] == user_data['name'], "Имя не совпадает"

    @allure.story('Создание пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, api_client, registered_user):
        user_data, _ = registered_user
        response = api_client.create_user(user_data)

        assert response.status_code == 403, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is False, "Ответ не содержит success:false"
        assert 'message' in data, "Нет сообщения об ошибке"

    @allure.story('Создание пользователя с неполными данными')
    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    def test_create_user_with_missing_field(self, api_client, user_data, field_to_remove):
        incomplete_data = user_data.copy()
        del incomplete_data[field_to_remove]

        response = api_client.create_user(incomplete_data)

        assert response.status_code == 403, f"Неверный код ответа при удалении поля {field_to_remove}"
        data = response.json()
        assert data.get('success') is False, "Ответ не содержит success:false"
        assert 'message' in data, "Нет сообщения об ошибке"