import allure

@allure.feature('Получение заказов пользователя')
class TestOrderGet:

    @allure.story('Получение заказов авторизованным пользователем')
    def test_get_orders_with_auth(self, api_client, registered_user, ingredient_ids):
        _, token = registered_user

        selected_ingredients = ingredient_ids[:2]
        api_client.create_order(selected_ingredients, token)

        response = api_client.get_user_orders(token)

        assert response.status_code == 200, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is True, "Ответ не содержит success:true"
        assert 'orders' in data, "Нет данных о заказах в ответе"

    @allure.story('Получение заказов неавторизованным пользователем')
    def test_get_orders_without_auth(self, api_client):
        response = api_client.get_user_orders()

        assert response.status_code == 401, "Неверный код ответа"
        data = response.json()
        assert data.get('success') is False, "Ответ не содержит success:false"
        assert 'message' in data, "Нет сообщения об ошибке"