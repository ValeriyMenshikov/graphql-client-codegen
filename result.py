
# ... Код клиента на основе GraphQL schema.json
from sgqlc.types import ContainerTypeMeta, non_null
from schema import *
from graphql.client import GraphQLClient
from graphql.errors import GraphQLClientError


class GraphQLApiClient:
    def __init__(self, host: str, headers: dict = None, disable_log: bool = False):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log
        self.client = GraphQLClient(
            host=self.host,
            schema=schema,
            base_headers=self.headers,
            disable_log=self.disable_log
        )

    @staticmethod
    def _convert_to_model(response: dict, query_name: str, model: ContainerTypeMeta):
        json_data = response.get('data', {}).get(query_name)
        if json_data:
            return model(json_data)
        raise GraphQLClientError(response)

    def account_current(self, access_token: String) -> EnvelopeOfUserDetails | dict:
        query_name = 'accountCurrent'
        mutation = self.client.mutation(name=query_name)
        mutation.account_current(
            access_token=access_token,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response

    def accounts(self, paging: PagingQueryInput, with_inactive: Boolean) -> AccountsResponse | dict:
        query_name = 'accounts'
        mutation = self.client.mutation(name=query_name)
        mutation.accounts(
            paging=paging,
            with_inactive=with_inactive,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountsResponse
        )
        return response

    def register_account(self, registration: RegistrationInput) -> AccountRegisterResponse | dict:
        query_name = 'registerAccount'
        mutation = self.client.mutation(name=query_name)
        mutation.register_account(
            registration=registration,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountRegisterResponse
        )
        return response

    def activate_account(self, activation_token: UUID) -> EnvelopeOfUser | dict:
        query_name = 'activateAccount'
        mutation = self.client.mutation(name=query_name)
        mutation.activate_account(
            activation_token=activation_token,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    def change_account_email(self, change_email: ChangeEmailInput) -> EnvelopeOfUser | dict:
        query_name = 'changeAccountEmail'
        mutation = self.client.mutation(name=query_name)
        mutation.change_account_email(
            change_email=change_email,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    def reset_account_password(self, reset_password: ResetPasswordInput) -> EnvelopeOfUser | dict:
        query_name = 'resetAccountPassword'
        mutation = self.client.mutation(name=query_name)
        mutation.reset_account_password(
            reset_password=reset_password,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    def change_account_password(self, change_password: ChangePasswordInput) -> EnvelopeOfUser | dict:
        query_name = 'changeAccountPassword'
        mutation = self.client.mutation(name=query_name)
        mutation.change_account_password(
            change_password=change_password,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    def update_account(self, access_token: String, user_data: UpdateUserInput) -> EnvelopeOfUserDetails | dict:
        query_name = 'updateAccount'
        mutation = self.client.mutation(name=query_name)
        mutation.update_account(
            access_token=access_token,
            user_data=user_data,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response

    def login_account(self, login: LoginCredentialsInput) -> AccountLoginResponse | dict:
        query_name = 'loginAccount'
        mutation = self.client.mutation(name=query_name)
        mutation.login_account(
            login=login,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountLoginResponse
        )
        return response

    def logout_account(self, access_token: String) -> non_null(MutationResult) | dict:
        query_name = 'logoutAccount'
        mutation = self.client.mutation(name=query_name)
        mutation.logout_account(
            access_token=access_token,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=non_null(MutationResult)
        )
        return response

    def logout_all_account(self, access_token: String) -> non_null(MutationResult) | dict:
        query_name = 'logoutAllAccount'
        mutation = self.client.mutation(name=query_name)
        mutation.logout_all_account(
            access_token=access_token,
        )
        response = self.client.request(query=mutation)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=non_null(MutationResult)
        )
        return response

    