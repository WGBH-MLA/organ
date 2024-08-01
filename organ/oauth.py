from os import getenv

from fastapi_oauth2.claims import Claims
from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config
from fastapi_oauth2.middleware import Auth
from fastapi_oauth2.middleware import User as OAuthUser
from social_core.backends.github import GithubOAuth2
from sqlmodel import Session

from organ.db import engine
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


async def on_auth(auth: Auth, user: OAuthUser):
    print('Auth success', auth, user)

    with Session(engine) as session:
        u: User | None = session.get(User, user.identity)
        if u is None:
            print('New user: ', user.identity)
            u = User(**dict(user))
        else:
            print('Update user: ', user.identity)
            u = u.model_copy(update=dict(user))
        session.add(u)
        session.commit()
