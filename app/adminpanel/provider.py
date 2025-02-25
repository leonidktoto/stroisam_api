from jwt import InvalidTokenError
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from app.users import auth
from app.users.schemas import SUsers
from app.users.token import (
    ACCESS_TOKEN_TYPE,
    auth_user_set_cookie,
    create_access_token,
)
from app.users.validation import (
    get_user_by_token_sub,
    validate_auth_user,
    validate_token_type,
)


class MyAuthProvider(AuthProvider):
    def validate_admin_user(self, user: SUsers):
        return True if user.type_user_id == 2 else False

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError({"username": "Ensure username has at least 03 characters"})
        try:
            user = await validate_auth_user(username, password)
        except Exception:
            raise LoginFailed("Invalid username or password")

        if not self.validate_admin_user(user):
            raise LoginFailed("admin validation error")

        access_token = create_access_token(user)
        auth_user_set_cookie(response, ACCESS_TOKEN_TYPE, access_token)
        return response

    async def is_authenticated(self, request) -> bool:

        token = request.cookies.get(ACCESS_TOKEN_TYPE)
        if not token:
            return False

        try:
            payload = auth.decode_jwt(token)
            validate_token_type(payload, ACCESS_TOKEN_TYPE)
            user = await get_user_by_token_sub(payload)
        except InvalidTokenError:
            return False

        if not self.validate_admin_user(user):
            return False
        request.state.user = user

        return True

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        custom_app_title = "Привет, " + user.first_name + "!"
        # Update logo url according to current_user
        # custom_logo_url = None
        return AdminConfig(
            app_title=custom_app_title,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        # photo_url = None
        return AdminUser(username=user.first_name)

    async def logout(self, request: Request, response: Response) -> Response:
        response.delete_cookie(ACCESS_TOKEN_TYPE)
        return response
