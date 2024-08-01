from typing import Optional

from sqlmodel import Session, SQLModel, select
from starlette.datastructures import URL
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.routing import Route
from starlette_admin import BaseAdmin
from starlette_admin.auth import (
    AdminUser,
    AuthMiddleware,
    AuthProvider,
    login_not_required,
)
from starlette_admin.exceptions import FormValidationError, LoginFailed

from organ.config import AUTH0_CLIENT_ID, AUTH0_DOMAIN


class OAuthProvider(AuthProvider):
    async def is_authenticated(self, request: Request) -> bool:
        if request.get('user'):
            return True
        return False

    def get_admin_user(self, request: Request) -> Optional[AdminUser]:
        user = request.user
        return AdminUser(
            username=user['name'],
            photo_url=user['avatar_url'],
        )

    async def render_login(self, request: Request, admin: BaseAdmin):
        """Override the default login behavior to implement custom logic."""
        return RedirectResponse(
            url=URL(f'https://{AUTH0_DOMAIN}/authorize').include_query_params(
                client_id=AUTH0_CLIENT_ID,
                response_type='code',
                redirect_uri='http://localhost:9000/oauth2/github/authorize',
            )
        )

    async def render_logout(self, request: Request, admin: BaseAdmin) -> Response:
        """Override the default logout to implement custom logic"""
        response = RedirectResponse(
            url=URL(f'https://{AUTH0_DOMAIN}/v2/logout').include_query_params(
                returnTo=request.url_for(admin.route_name + ':index'),
                client_id=AUTH0_CLIENT_ID,
            )
        )
        response.delete_cookie('Authorization')
        return response

    @login_not_required
    async def handle_auth_callback(self, request: Request):
        return RedirectResponse(request.query_params.get('next'))

    def setup_admin(self, admin: BaseAdmin):
        super().setup_admin(admin)
        """add custom authentication callback route"""
        admin.routes.append(
            Route(
                '/auth0/authorize',
                self.handle_auth_callback,
                methods=['GET'],
                name='authorize_auth0',
            )
        )
