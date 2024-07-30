from os import getenv

from fastapi_oauth2.claims import Claims
from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config
from fastapi_oauth2.middleware import Auth, User
from social_core.backends.github import GithubOAuth2

from organ.db import get_async_session
from organ.models import User

github_client = OAuth2Client(
    backend=GithubOAuth2,
    client_id=getenv('OAUTH2_GITHUB_CLIENT_ID'),
    client_secret=getenv('OAUTH2_GITHUB_CLIENT_SECRET'),
    scope=['user:email'],
    claims=Claims(
        picture='avatar_url',
        identity=lambda user: f'{user.provider}:{user.id}',
    ),
)


oauth_config = OAuth2Config(
    allow_http=True,
    jwt_secret=getenv('JWT_SECRET'),
    jwt_expires=getenv('JWT_EXPIRES'),
    jwt_algorithm=getenv('JWT_ALGORITHM'),
    clients=[
        github_client,
    ],
)


async def on_auth(auth: Auth, user: User):
    print('Auth success', auth, user)

    with get_async_session() as session:
        session.add(User(**user.model_dump()))
        session.commit()
