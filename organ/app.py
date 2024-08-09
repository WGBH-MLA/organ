import logfire
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_oauth2.middleware import OAuth2Middleware
from fastapi_oauth2.router import router as oauth2_router
from sqlmodel import SQLModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import RedirectResponse, Route
from starlette_admin.contrib.sqlmodel import Admin

from organ._version import __version__
from organ.auth import OAuthProvider
from organ.config import ORGAN_SECRET
from organ.crud import orgs, ov_catalog
from organ.db import engine
from organ.models import OpenVaultCatalog, Organization, User
from organ.oauth import is_user_authenticated, oauth_config, on_auth
from organ.views import OpenVaultCatalogView, OrganizationView, UserView


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
app.add_middleware(SessionMiddleware, secret_key=ORGAN_SECRET)
app.include_router(orgs, dependencies=[Depends(is_user_authenticated)])
app.include_router(ov_catalog, dependencies=[Depends(is_user_authenticated)])

# Add static files
app.mount("/static", StaticFiles(directory="static"), name="static")

admin = Admin(
    engine,
    title='Organ',
    templates_dir='templates',
    auth_provider=OAuthProvider(
        logout_path="/oauth2/logout",
    ),
    logo_url='/static/GBH_Archives.png',
)

# Add views
admin.add_view(UserView(User, icon="fa fa-users"))
admin.add_view(OrganizationView(Organization, icon="fa fa-box"))
admin.add_view(OpenVaultCatalogView(OpenVaultCatalog, icon="fa fa-vault"))

admin.mount_to(app)
