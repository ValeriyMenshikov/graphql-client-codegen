from collections import namedtuple
from datetime import datetime

import pytest

from graphql_api import GraphQLApiClient
import structlog

from schema import RegistrationInput

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def client():
    return GraphQLApiClient(host='http://localhost:5051/graphql')


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%Y_%m_%d_%H_%M_%S")
    login = f'login_{data}'
    email = f'login_{data}@mail.ru'
    password = '12345678'
    user = namedtuple('User', 'login, email, password')
    return user(login=login, email=email, password=password)


# @pytest.fixture
# def activated_user(prepare_user, client):
#     registration = RegistrationInput(
#         email=prepare_user.email,
#         login=prepare_user.login,
#         password=prepare_user.password,
#     )
#     client.register_account(registration=registration)
#     def get_activa