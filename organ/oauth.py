from os import getenv

from fastapi import HTTPException, Request
from fastapi_oauth2.claims import Claims
from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config
from fastapi_oauth2.middleware import Auth
from fastapi_oauth2.middleware import User as OAuthUser
from social_core.backends.github import GithubOAuth2
from sqlmodel import Session
from loguru import logger as log

from organ.db import engine
from organ.models import User
from organ import config

github_client = OAuth2Client(
    backend=GithubOAuth2,
    client_id=config.OAUTH2_GITHUB_CLIENT_ID,
    client_secret=config.OAUTH2_GITHUB_CLIENT_SECRET,
    scope=['user:email'],
    claims=Claims(
        picture='avatar_url',
        identity=lambda user: f'{user.provider}:{user.id}',
    ),
)


oauth_config = OAuth2Config(
    allow_http=True,
    jwt_secret=config.JWT_SECRET,
    jwt_expires=config.JWT_EXPIRES,
    jwt_algorithm=config.JWT_ALGORITHM,
    clients=[
        github_client,
    ],
)


async def on_auth(auth: Auth, user: OAuthUser) -> None:
    log.debug('Auth success', auth, user)

    # TODO: This function currently runs on every authenticated request, which is not ideal.
    # We should only run this after a new token is issued.
    with Session(engine) as session:
        u: User | None = session.get(User, user.identity)
        if u is None:
            log.success('New user: ', user.identity)
            u = User(**dict(user))
            session.add(u)
            session.commit()


def is_user_authenticated(request: Request) -> OAuthUser:
    user = request.get('user')
    if not user:
        raise HTTPException(401, detail="User not authenticated")
    return OAuthUser(**user)
