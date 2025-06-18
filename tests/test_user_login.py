import allure

@allure.feature('Логин пользователя')
class TestUserLogin:

    @allure.story('Логин под существующим пользователем')
    def test_login_valid_user(self, api_client, registered_user):
        user_data, _ = registered_user
        credentials = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        response = api_client.login_user(credentials)

        assert response.status_code == 200, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is True, "Ответ не содержит success:true"
        assert 'accessToken' in data, "Не получен токен доступа"
        assert 'user' in data, "Нет данных пользователя в ответе"

    @allure.story('Логин с неверным логином и паролем')
    def test_login_invalid_credentials(self, api_client, user_data):
        invalid_credentials = {
            "email": user_data["email"],
            "password": "wrongpassword123"
        }

        response = api_client.login_user(invalid_credentials)

        assert response.status_code == 401, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is False, "Ответ не содержит success:false"
        assert 'message' in data, "Нет сообщения об ошибке"