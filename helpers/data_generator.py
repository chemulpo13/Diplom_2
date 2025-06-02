import random
import string
from faker import Faker

fake = Faker()

def generate_user_data():
    fake = Faker()
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        'email': f"{fake.user_name()}_{random_suffix}@example.com",
        'password': fake.password(length=10),
        'name': fake.name()
    }

def generate_update_data():
    return {
        "email": fake.email(),
        "name": fake.name()
    }