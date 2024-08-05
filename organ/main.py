from fastapi import FastAPI
from sqlmodel import Session, SQLModel
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import RedirectResponse, Route
from starlette_admin.contrib.sqlmodel import Admin, ModelView

from organ._version import __version__
from organ.api import org
from organ.auth import CustomAuthProvider
from organ.config import ENVIRONMENT, ORGAN_SECRET
from organ.crud import orgs
from organ.db import engine, get_user
from organ.models import Organization, User
from organ.views import OrganizationView


def init_db():
    SQLModel.metadata.create_all(engine)


def create_admin_user():
    if ENVIRONMENT != "development":
        return
    with Session(engine) as session:
        if not get_user("mrman"):
            session.add(
                User(username="mrman", full_name="Mr. Man", password="coolpass")
            )
        session.commit()


def redirect_to_admin(request):
    return RedirectResponse(url="/admin")


main = FastAPI(
    on_startup=[init_db, create_admin_user],
    routes=[
        Route("/", redirect_to_admin),
    ],
)

main.include_router(org, prefix="/org", tags=["org"])
main.include_router(orgs)

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
