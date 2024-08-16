from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from starlette.templating import Jinja2Templates
from jinja2 import TemplateNotFound

from starlette_admin.base import BaseAdmin
from starlette.status import (
    HTTP_303_SEE_OTHER,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


# Указываем путь к папке с шаблонами
templates = Jinja2Templates(directory="app/adminpanel/templates")

users = {
    "admin": {
        "name": "Administrator",
        "avatar": "avatar.png",
        "company_logo_url": "avatar.png",
        "roles": ["read", "create", "edit", "delete", "action_make_published"],
    },
    "johndoe": {
        "name": "John Doe",
        "avatar": None,  # user avatar is optional
        "roles": ["read", "create", "edit", "action_make_published"],
    },
    "viewer": {"name": "Viewer", "avatar": None, "roles": ["read"]},
}


class MyAuthProvider(AuthProvider):
    """
    This is for demo purpose, it's not a better
    way to save and validate user credentials
    """

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

        if username in users and password == "password":
            """Save `username` in session"""
            request.session.update({"username": username})

            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = users.get(request.session["username"])
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        custom_app_title = "Hello, " + user["name"] + "!"
        # Update logo url according to current_user
        custom_logo_url = None
        return AdminConfig(
            app_title=custom_app_title,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        return AdminUser(username=user["name"])

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response

"""
    async def render_login(self, request: Request, admin: "BaseAdmin") -> Response:
  
        if request.method == "GET":
            return admin.templates.TemplateResponse(
                "login.html",
                {"request": request, "_is_login_path": True},
            )
        form = await request.form()
        try:
            return await self.login(
                form.get("username"),  # type: ignore
                form.get("password"),  # type: ignore
                form.get("remember_me") == "on",
                request,
                RedirectResponse(
                    request.query_params.get("next")
                    or request.url_for(admin.route_name + ":index"),
                    status_code=HTTP_303_SEE_OTHER,
                ),
            )
        except FormValidationError as errors:
            return admin.templates.TemplateResponse(
                "login.html",
                {"request": request, "form_errors": errors, "_is_login_path": True},
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except LoginFailed as error:
            return admin.templates.TemplateResponse(
                "login.html",
                {"request": request, "error": error.msg, "_is_login_path": True},
                status_code=HTTP_400_BAD_REQUEST,
            )"""