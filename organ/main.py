from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

# from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import RedirectResponse, Route

# from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette_admin.contrib.sqlmodel import Admin, ModelView

from organ._version import __version__
from organ.api import org
from organ.auth import CustomAuthProvider
from organ.config import ENVIRONMENT, ORGAN_SECRET
from organ.db import engine, get_user
from organ.models import Organization, User
from organ.views import OrganizationView


def init_db():

    SQLModel.metadata.create_all(engine)


def create_admin_user():
    if ENVIRONMENT == "development":
        with Session(engine) as session:
            if not get_user("mrman"):
                session.add(
                    User(username="mrman", full_name="Mr. Man", password="coolpass")
                )

                session.add(
                    Organization(name="Cool Org", shortname="WCORG", state="CO")
                )

                return session.commit()


def redirect_to_admin(request):
    return RedirectResponse(url="/admin")


main = FastAPI(
    on_startup=[init_db, create_admin_user],
    routes=[
        Route("/", redirect_to_admin),
        # Route("/org/{uid}", org_by_uid, methods=["GET"]),
        # Route("/org", org_by_uid, methods=["POST"])
    ],
)

main.include_router(org, prefix="/org", tags=["org"])

admin = Admin(
    engine,
    title='Organ',
    templates_dir='templates',
    statics_dir='static',
    auth_provider=CustomAuthProvider(login_path="/sign-in", logout_path="/sign-out"),
    middlewares=[Middleware(SessionMiddleware, secret_key=ORGAN_SECRET)],
)

# Add views
admin.add_view(ModelView(User, icon="fa fa-users"))
admin.add_view(OrganizationView(Organization, icon="fa fa-box"))
admin.mount_to(main)
