from typing import Optional

from sqlmodel import Session, SQLModel, select
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from organ.db import engine, get_user
from organ.models import User

# users = {
#     "admin": {
#         "name": "Admin",
#         "avatar": "avatars/01.png",
#         "roles": ["admin"],
#     },
#     "demo": {
#         "name": "John Doe",
#         "avatar": None,
#         "roles": ["demo"],
#     },
# }


class CustomAuthProvider(AuthProvider):
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
        {"username": "Please ensure that your username has at least 3 characters"}
      )

    # load user from db
    user = get_user(username)
    if user and password == user.password:
      """Save `username` in session"""
      request.session.update({"username": username})
      return response

    raise LoginFailed("Invalid username or password.")

  async def is_authenticated(self, request) -> bool:
    print(request.method == "GET")
    if request.method == "GET" and str(request.url).startswith("/admin/api/organization"):
      # allow unauthenticated read access
      return True

    user = get_user(request.session.get("username", None))
    if user:
      """
      Save current `user` object in the request state. Can be used later
      to restrict access to connected user.
      """
      request.state.user = user.username
      return True

    return False

  def get_admin_user(self, request: Request) -> Optional[AdminUser]:
    username = request.state.user  # Retrieve current user
    
    return AdminUser(username=username)

  async def logout(self, request: Request, response: Response) -> Response:
    request.session.clear()
    return response
