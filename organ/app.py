import logfire
from fastapi import FastAPI
from fastapi_oauth2.middleware import OAuth2Middleware
from fastapi_oauth2.router import router as oauth2_router
from sqlmodel import SQLModel
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import RedirectResponse, Route
from starlette_admin.contrib.sqlmodel import Admin, ModelView

from organ._version import __version__
from organ.api import org
from organ.auth import OAuthProvider
from organ.config import ORGAN_SECRET
from organ.crud import orgs
from organ.db import engine
from organ.models import Organization, User
from organ.oauth import oauth_config, on_auth
from organ.views import OrganizationView


def init_db():
    logfire.info(f'Organ version: {__version__}')
    SQLModel.metadata.create_all(engine)


def redirect_to_admin(request):
    return RedirectResponse(url="/admin")


app = FastAPI(
    on_startup=[init_db],
    routes=[
        Route("/", redirect_to_admin),
    ],
)
logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record='all'))
logfire.instrument_fastapi(app)


app.include_router(oauth2_router, tags=["auth"])
app.add_middleware(OAuth2Middleware, config=oauth_config, callback=on_auth)
app.include_router(org, prefix="/org", tags=["org"])
app.include_router(orgs)

admin = Admin(
    engine,
    title='Organ',
    templates_dir='templates',
    statics_dir='static',
    auth_provider=OAuthProvider(
        logout_path="/oauth2/logout",
    ),
    middlewares=[Middleware(SessionMiddleware, secret_key=ORGAN_SECRET)],
    logo_url='static/GBH_Archives.png',
)

# Add views
admin.add_view(ModelView(User, icon="fa fa-users"))
admin.add_view(OrganizationView(Organization, icon="fa fa-box"))


admin.mount_to(app)
