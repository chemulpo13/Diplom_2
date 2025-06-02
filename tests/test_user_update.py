import allure
from helpers.data_generator import generate_update_data

@allure.feature('Изменение данных пользователя')
class TestUserUpdate:

    @allure.story('Изменение данных с авторизацией')
    def test_update_authorized_user(self, api_client, registered_user):
        _, token = registered_user
        new_data = generate_update_data()

        response = api_client.update_user(new_data, token)

        assert response.status_code == 200, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is True, "Ответ не содержит success:true"
        assert data['user']['email'] == new_data['email'], "Email не обновился"
        assert data['user']['name'] == new_data['name'], "Имя не обновилось"

    @allure.story('Изменение данных без авторизации')
    def test_update_unauthorized_user(self, api_client):
        new_data = generate_update_data()

        response = api_client.update_user(new_data)

        assert response.status_code == 401, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is False, "Ответ не содержит success:false"
        assert 'message' in data, "Нет сообщения об ошибке"