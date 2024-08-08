from typing import Optional

from starlette.datastructures import URL
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette_admin import BaseAdmin
from starlette_admin.auth import AdminUser, AuthProvider


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

    async def render_logout(self, request: Request, admin: BaseAdmin) -> Response:
        """Override the default logout to implement custom logic"""
        return RedirectResponse(url=URL('/oauth2/logout'))
