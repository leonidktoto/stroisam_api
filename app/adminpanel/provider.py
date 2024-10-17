from jwt import InvalidTokenError
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed, StarletteAdminException


from starlette_admin.base import BaseAdmin
from starlette.status import (
    HTTP_303_SEE_OTHER,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.users import auth
from app.users.schemas import SUsers
from app.users.token import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, auth_user_set_cookie, create_access_token, create_refresh_token
from app.users.validation import get_current_token_payload, get_user_by_token_sub, validate_auth_user, validate_token_type


# Указываем путь к папке с шаблонами
#templates = Jinja2Templates(directory="app/adminpanel/templates")



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
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )
        try:
            user = await validate_auth_user(username, password)
        except:
            raise LoginFailed("Invalid username or password")

        if not self.validate_admin_user(user):
            raise  LoginFailed("admin validation error")

        access_token = create_access_token(user)
        auth_user_set_cookie(response, ACCESS_TOKEN_TYPE, access_token)
        return response

            


    async def is_authenticated(self, request) -> bool:

        token=request.cookies.get(ACCESS_TOKEN_TYPE)  
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
        custom_app_title = "Hello, " + user.first_name + "!"
        # Update logo url according to current_user
        custom_logo_url = None
        return AdminConfig(
            app_title=custom_app_title,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        return AdminUser(username=user.first_name)

    async def logout(self, request: Request, response: Response) -> Response:
        response.delete_cookie(ACCESS_TOKEN_TYPE)
        return response

    
            
            

