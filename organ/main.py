from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select, Session

from starlette.responses import JSONResponse
from starlette.routing import Route, RedirectResponse
# from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
# from starlette.applications import Starlette

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from starlette_admin.contrib.sqlmodel import Admin, ModelView

from organ._version import __version__
from organ.config import ORGAN_SECRET, ENVIRONMENT
from organ.db import engine, get_user
from organ.auth import CustomAuthProvider
from organ.models import Organization, User
from organ.views import OrganizationView
# from organ.config import STATIC_DIR, TEMPLATES_DIR

templates = Jinja2Templates(directory="templates")

def init_db():
  SQLModel.metadata.create_all(engine)

def create_admin_user():
  if ENVIRONMENT == "development":
    with Session(engine) as session:
      if not get_user("mrman"):
        session.add( User(username="mrman", full_name="Mr. Man", password="coolpass") )

        session.add( Organization(name="Cool Org", shortname="WCORG", state="CO") )

        return session.commit()

def redirect_to_admin(request):
  return RedirectResponse(url="/admin")

def serialize_org(org):
  return {
    "uid": org.uid,
    "name": org.name,
    "shortname": org.shortname,
    "state": org.state,
    "url": org.url,
    "logo_url": org.logo_url,
    "about": org.about,
    "productions": org.productions,
  }

main = FastAPI(
  on_startup=[ init_db, create_admin_user ],
  routes=[
    Route("/", redirect_to_admin),
    # Route("/org/{uid}", org_by_uid, methods=["GET"]),
    # Route("/org", org_by_uid, methods=["POST"])
  ]
)

# get an org by uid
@main.get("/org/{uid}")
def org_by_uid(uid):
  with Session(engine) as session:
    org = session.exec( select(Organization).where(Organization.uid == uid)  ).first()

    if org:
      return JSONResponse({"org": serialize_org(org)})
    else:
      return JSONResponse({"error": "Organzation not found", "org": None})

# search for orgs based on any field
@main.get("/orgs")
def get_orgs(uid: str = None, name: str = None, shortname: str = None, state: str = None, url: str = None, logo_url: str = None, about: str = None, productions: str = None):
  with Session(engine) as session:

    search = select(Organization)

    if uid:
      search = search.where(Organization.uid.like("%" + uid + "%"))
    if name:
      search = search.where(Organization.name.like("%" + name + "%"))
    if shortname:
      search = search.where(Organization.shortname.like("%" + shortname + "%"))
    if state:
      search = search.where(Organization.state.like("%" + state + "%"))
    if url:
      search = search.where(Organization.url.like("%" + url + "%"))
    if logo_url:
      search = search.where(Organization.logo_url.like("%" + logo_url + "%"))
    if about:
      search = search.where(Organization.about.like("%" + about + "%"))
    if productions:
      search = search.where(Organization.productions.like("%" + productions + "%"))

    orgs = session.exec( search ).all()

    if orgs:
      return JSONResponse({"orgs": list( map(lambda o: serialize_org(o), orgs ) ) })
    else:
      return JSONResponse({"error": "No matching results...", "org": None})

@main.post("/org")
def create_org(name: str = None, shortname: str = None, state: str = None, url: str = None, logo_url: str = None, about: str = None, productions: str = None):

  if name and shortname:
    with Session(engine) as session:
      org = Organization(name=name, shortname=shortname, state=state, url=url, logo_url=logo_url, about=about, productions=productions)
      print(f"my org is { org }")
      session.add(org)
      session.commit()

      org = session.exec( select.where(Organization.name == name) ).first()

      return JSONResponse({"org": serialize_org( org ) })

  else:
    # which field was missing?
    fieldname = "name" if shortname else "shortname"

    return JSONResponse({"error": f"Missing value for required field: { fieldname }", "org": None})


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
