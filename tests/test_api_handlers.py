from schema import *

gemail = 'graphql_gen@test.ru'
glogin = gpassword = 'graphql_gen'


def test_register_account(client, prepare_user):
    email = prepare_user.email
    login = prepare_user.login
    password = prepare_user.password

    registration = RegistrationInput(
        email=email,
        login=login,
        password=password,
    )
    client.register_account(registration=registration)


def test_accounts(client):
    response = client.accounts(paging=PagingQueryInput(), with_inactive=True)
    assert response.paging
    assert response.users


def test_login_account(client):
    response = client.login_account(login=LoginCredentialsInput(login=glogin, password=gpassword, remember_me=False))
    assert response.token


def test_activate_account(client):
    response = client.activate_account(activation_token='c9cad851-6f3d-4d5a-89cf-b7a69ce564bf')
    assert response.resource
