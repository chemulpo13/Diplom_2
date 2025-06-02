import pytest
import allure
import random
from helpers.api_client import ApiClient
from helpers.data_generator import generate_user_data

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def user_data():
    return generate_user_data()

@pytest.fixture
def registered_user(api_client, user_data):
    response = api_client.create_user(user_data)
    token = response.json().get('accessToken', '')

    yield user_data, token

@pytest.fixture
def ingredient_ids(api_client):
    response = api_client.get_ingredients()
    ingredients = response.json().get('data', [])
    ingredient_ids = [ingredient['_id'] for ingredient in ingredients]

    yield ingredient_ids