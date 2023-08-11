import sgqlc.types
import sgqlc.types.datetime

schema = sgqlc.types.Schema()


########################################################################
# Scalars and Enumerations
########################################################################
class AccessPolicy(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CHAT_BAN', 'DEMOCRATIC_BAN', 'FULL_BAN', 'NOT_SPECIFIED', 'RESTRICT_CONTENT_EDITING')


class BbParseMode(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CHAT', 'COMMON', 'INFO', 'POST')


Boolean = sgqlc.types.Boolean


class ColorSchema(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CLASSIC', 'CLASSIC_PALE', 'MODERN', 'NIGHT', 'PALE')


DateTime = sgqlc.types.datetime.DateTime

Int = sgqlc.types.Int


class MutationResult(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('OK',)


String = sgqlc.types.String


class UUID(sgqlc.types.Scalar):
    __schema__ = schema


class UserRole(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('ADMINISTRATOR', 'GUEST', 'NANNY_MODERATOR', 'PLAYER', 'REGULAR_MODERATOR', 'SENIOR_MODERATOR')


########################################################################
# Input Objects
########################################################################
class ChangeEmailInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('login', 'password', 'email')
    login = sgqlc.types.Field(String, graphql_name='login')
    password = sgqlc.types.Field(String, graphql_name='password')
    email = sgqlc.types.Field(String, graphql_name='email')


class ChangePasswordInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('login', 'token', 'old_password', 'new_password')
    login = sgqlc.types.Field(String, graphql_name='login')
    token = sgqlc.types.Field(UUID, graphql_name='token')
    old_password = sgqlc.types.Field(String, graphql_name='oldPassword')
    new_password = sgqlc.types.Field(String, graphql_name='newPassword')


class LoginCredentialsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('login', 'password', 'remember_me')
    login = sgqlc.types.Field(String, graphql_name='login')
    password = sgqlc.types.Field(String, graphql_name='password')
    remember_me = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='rememberMe')


class PagingQueryInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('skip', 'number', 'size')
    skip = sgqlc.types.Field(Int, graphql_name='skip')
    number = sgqlc.types.Field(Int, graphql_name='number')
    size = sgqlc.types.Field(Int, graphql_name='size')


class PagingSettingsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = (
    'posts_per_page', 'comments_per_page', 'topics_per_page', 'messages_per_page', 'entities_per_page')
    posts_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='postsPerPage')
    comments_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsPerPage')
    topics_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='topicsPerPage')
    messages_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='messagesPerPage')
    entities_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='entitiesPerPage')


class RegistrationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('login', 'email', 'password')
    login = sgqlc.types.Field(String, graphql_name='login')
    email = sgqlc.types.Field(String, graphql_name='email')
    password = sgqlc.types.Field(String, graphql_name='password')


class ResetPasswordInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('login', 'email')
    login = sgqlc.types.Field(String, graphql_name='login')
    email = sgqlc.types.Field(String, graphql_name='email')


class UpdateUserInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('login', 'status', 'rating_disabled', 'name', 'location', 'icq', 'skype', 'info', 'settings')
    login = sgqlc.types.Field(String, graphql_name='login')
    status = sgqlc.types.Field(String, graphql_name='status')
    rating_disabled = sgqlc.types.Field(Boolean, graphql_name='ratingDisabled')
    name = sgqlc.types.Field(String, graphql_name='name')
    location = sgqlc.types.Field(String, graphql_name='location')
    icq = sgqlc.types.Field(String, graphql_name='icq')
    skype = sgqlc.types.Field(String, graphql_name='skype')
    info = sgqlc.types.Field(String, graphql_name='info')
    settings = sgqlc.types.Field('UserSettingsInput', graphql_name='settings')


class UserSettingsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'nanny_greetings_message', 'color_schema', 'paging')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    nanny_greetings_message = sgqlc.types.Field(String, graphql_name='nannyGreetingsMessage')
    color_schema = sgqlc.types.Field(sgqlc.types.non_null(ColorSchema), graphql_name='colorSchema')
    paging = sgqlc.types.Field(PagingSettingsInput, graphql_name='paging')


########################################################################
# Output Objects and Interfaces
########################################################################
class AccountLoginResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('token', 'user')
    token = sgqlc.types.Field(String, graphql_name='token')
    user = sgqlc.types.Field('EnvelopeOfUser', graphql_name='user')


class AccountRegisterResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'login')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    login = sgqlc.types.Field(String, graphql_name='login')


class AccountsResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('users', 'paging')
    users = sgqlc.types.Field(sgqlc.types.list_of('GeneralUser'), graphql_name='users')
    paging = sgqlc.types.Field('PagingResult', graphql_name='paging')


class EnvelopeOfUser(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('resource',)
    resource = sgqlc.types.Field('User', graphql_name='resource')


class EnvelopeOfUserDetails(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('resource',)
    resource = sgqlc.types.Field('UserDetails', graphql_name='resource')


class GeneralUser(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('user_id', 'login', 'email', 'role', 'access_policy', 'last_visit_date', 'original_picture_url',
                       'medium_picture_url', 'small_picture_url', 'status', 'name', 'location', 'rating_disabled',
                       'quality_rating', 'quantity_rating', 'is_authenticated')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='userId')
    login = sgqlc.types.Field(String, graphql_name='login')
    email = sgqlc.types.Field(String, graphql_name='email')
    role = sgqlc.types.Field(sgqlc.types.non_null(UserRole), graphql_name='role')
    access_policy = sgqlc.types.Field(sgqlc.types.non_null(AccessPolicy), graphql_name='accessPolicy')
    last_visit_date = sgqlc.types.Field(DateTime, graphql_name='lastVisitDate')
    original_picture_url = sgqlc.types.Field(String, graphql_name='originalPictureUrl')
    medium_picture_url = sgqlc.types.Field(String, graphql_name='mediumPictureUrl')
    small_picture_url = sgqlc.types.Field(String, graphql_name='smallPictureUrl')
    status = sgqlc.types.Field(String, graphql_name='status')
    name = sgqlc.types.Field(String, graphql_name='name')
    location = sgqlc.types.Field(String, graphql_name='location')
    rating_disabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='ratingDisabled')
    quality_rating = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='qualityRating')
    quantity_rating = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='quantityRating')
    is_authenticated = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isAuthenticated')


class InfoBbText(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('parse_mode', 'value')
    parse_mode = sgqlc.types.Field(sgqlc.types.non_null(BbParseMode), graphql_name='parseMode')
    value = sgqlc.types.Field(String, graphql_name='value')


class LoginEvent(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('login', 'timestamp')
    login = sgqlc.types.Field(String, graphql_name='login')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='timestamp')


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
    'register_account', 'activate_account', 'change_account_email', 'reset_account_password', 'change_account_password',
    'update_account', 'login_account', 'logout_account', 'logout_all_account')
    register_account = sgqlc.types.Field(AccountRegisterResponse, graphql_name='registerAccount',
                                         args=sgqlc.types.ArgDict((
                                             ('registration',
                                              sgqlc.types.Arg(RegistrationInput, graphql_name='registration',
                                                              default=None)),
                                         ))
                                         )
    activate_account = sgqlc.types.Field(EnvelopeOfUser, graphql_name='activateAccount', args=sgqlc.types.ArgDict((
        ('activation_token', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='activationToken', default=None)),
    ))
                                         )
    change_account_email = sgqlc.types.Field(EnvelopeOfUser, graphql_name='changeAccountEmail',
                                             args=sgqlc.types.ArgDict((
                                                 ('change_email',
                                                  sgqlc.types.Arg(ChangeEmailInput, graphql_name='changeEmail',
                                                                  default=None)),
                                             ))
                                             )
    reset_account_password = sgqlc.types.Field(EnvelopeOfUser, graphql_name='resetAccountPassword',
                                               args=sgqlc.types.ArgDict((
                                                   ('reset_password',
                                                    sgqlc.types.Arg(ResetPasswordInput, graphql_name='resetPassword',
                                                                    default=None)),
                                               ))
                                               )
    change_account_password = sgqlc.types.Field(EnvelopeOfUser, graphql_name='changeAccountPassword',
                                                args=sgqlc.types.ArgDict((
                                                    ('change_password',
                                                     sgqlc.types.Arg(ChangePasswordInput, graphql_name='changePassword',
                                                                     default=None)),
                                                ))
                                                )
    update_account = sgqlc.types.Field(EnvelopeOfUserDetails, graphql_name='updateAccount', args=sgqlc.types.ArgDict((
        ('access_token', sgqlc.types.Arg(String, graphql_name='accessToken', default=None)),
        ('user_data', sgqlc.types.Arg(UpdateUserInput, graphql_name='userData', default=None)),
    ))
                                       )
    login_account = sgqlc.types.Field(AccountLoginResponse, graphql_name='loginAccount', args=sgqlc.types.ArgDict((
        ('login', sgqlc.types.Arg(LoginCredentialsInput, graphql_name='login', default=None)),
    ))
                                      )
    logout_account = sgqlc.types.Field(sgqlc.types.non_null(MutationResult), graphql_name='logoutAccount',
                                       args=sgqlc.types.ArgDict((
                                           ('access_token',
                                            sgqlc.types.Arg(String, graphql_name='accessToken', default=None)),
                                       ))
                                       )
    logout_all_account = sgqlc.types.Field(sgqlc.types.non_null(MutationResult), graphql_name='logoutAllAccount',
                                           args=sgqlc.types.ArgDict((
                                               ('access_token',
                                                sgqlc.types.Arg(String, graphql_name='accessToken', default=None)),
                                           ))
                                           )


class PagingResult(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('total_pages_count', 'total_entities_count', 'current_page', 'page_size', 'entity_number')
    total_pages_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalPagesCount')
    total_entities_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalEntitiesCount')
    current_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='currentPage')
    page_size = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageSize')
    entity_number = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='entityNumber')


class PagingSettings(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
    'posts_per_page', 'comments_per_page', 'topics_per_page', 'messages_per_page', 'entities_per_page')
    posts_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='postsPerPage')
    comments_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentsPerPage')
    topics_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='topicsPerPage')
    messages_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='messagesPerPage')
    entities_per_page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='entitiesPerPage')


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('account_current', 'accounts')
    account_current = sgqlc.types.Field(EnvelopeOfUserDetails, graphql_name='accountCurrent', args=sgqlc.types.ArgDict((
        ('access_token', sgqlc.types.Arg(String, graphql_name='accessToken', default=None)),
    ))
                                        )
    accounts = sgqlc.types.Field(AccountsResponse, graphql_name='accounts', args=sgqlc.types.ArgDict((
        ('paging', sgqlc.types.Arg(PagingQueryInput, graphql_name='paging', default=None)),
        ('with_inactive', sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name='withInactive', default=None)),
    ))
                                 )


class Rating(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('enabled', 'quality', 'quantity')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    quality = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='quality')
    quantity = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='quantity')


class Subscription(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('user_login',)
    user_login = sgqlc.types.Field(LoginEvent, graphql_name='userLogin')


class User(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
    'login', 'roles', 'medium_picture_url', 'small_picture_url', 'status', 'rating', 'online', 'name', 'location',
    'registration')
    login = sgqlc.types.Field(String, graphql_name='login')
    roles = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UserRole)), graphql_name='roles')
    medium_picture_url = sgqlc.types.Field(String, graphql_name='mediumPictureUrl')
    small_picture_url = sgqlc.types.Field(String, graphql_name='smallPictureUrl')
    status = sgqlc.types.Field(String, graphql_name='status')
    rating = sgqlc.types.Field(Rating, graphql_name='rating')
    online = sgqlc.types.Field(DateTime, graphql_name='online')
    name = sgqlc.types.Field(String, graphql_name='name')
    location = sgqlc.types.Field(String, graphql_name='location')
    registration = sgqlc.types.Field(DateTime, graphql_name='registration')


class UserDetails(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
    'icq', 'skype', 'original_picture_url', 'info', 'settings', 'login', 'roles', 'medium_picture_url',
    'small_picture_url', 'status', 'rating', 'online', 'name', 'location', 'registration')
    icq = sgqlc.types.Field(String, graphql_name='icq')
    skype = sgqlc.types.Field(String, graphql_name='skype')
    original_picture_url = sgqlc.types.Field(String, graphql_name='originalPictureUrl')
    info = sgqlc.types.Field(InfoBbText, graphql_name='info')
    settings = sgqlc.types.Field('UserSettings', graphql_name='settings')
    login = sgqlc.types.Field(String, graphql_name='login')
    roles = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UserRole)), graphql_name='roles')
    medium_picture_url = sgqlc.types.Field(String, graphql_name='mediumPictureUrl')
    small_picture_url = sgqlc.types.Field(String, graphql_name='smallPictureUrl')
    status = sgqlc.types.Field(String, graphql_name='status')
    rating = sgqlc.types.Field(Rating, graphql_name='rating')
    online = sgqlc.types.Field(DateTime, graphql_name='online')
    name = sgqlc.types.Field(String, graphql_name='name')
    location = sgqlc.types.Field(String, graphql_name='location')
    registration = sgqlc.types.Field(DateTime, graphql_name='registration')


class UserSettings(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('color_schema', 'nanny_greetings_message', 'paging')
    color_schema = sgqlc.types.Field(sgqlc.types.non_null(ColorSchema), graphql_name='colorSchema')
    nanny_greetings_message = sgqlc.types.Field(String, graphql_name='nannyGreetingsMessage')
    paging = sgqlc.types.Field(PagingSettings, graphql_name='paging')


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = Subscription
