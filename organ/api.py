from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from organ.db import engine
from organ.models import Organization

org = APIRouter()


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


# get an org by uid
@org.get("/{uid}")
def org_by_uid(uid):
    with Session(engine) as session:
        org = session.exec(select(Organization).where(Organization.uid == uid)).first()

        if org:
            return JSONResponse({"org": serialize_org(org)})
        else:
            return JSONResponse({"error": "Organzation not found", "org": None})


# search for orgs based on any field
@org.get("/")
def get_orgs(
    uid: str = None,
    name: str = None,
    shortname: str = None,
    state: str = None,
    url: str = None,
    logo_url: str = None,
    about: str = None,
    productions: str = None,
):
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
            search = search.where(
                Organization.productions.like("%" + productions + "%")
            )

        orgs = session.exec(search).all()

        if orgs:
            return JSONResponse({"orgs": list(map(lambda o: serialize_org(o), orgs))})
        else:
            return JSONResponse({"error": "No matching results...", "org": None})


@org.post("/")
def create_org(
    name: str = None,
    shortname: str = None,
    state: str = None,
    url: str = None,
    logo_url: str = None,
    about: str = None,
    productions: str = None,
):

    if name and shortname:
        with Session(engine) as session:
            org = Organization(
                name=name,
                shortname=shortname,
                state=state,
                url=url,
                logo_url=logo_url,
                about=about,
                productions=productions,
            )
            print(f"my org is { org }")
            session.add(org)
            session.commit()

            org = session.exec(select.where(Organization.name == name)).first()

            return JSONResponse({"org": serialize_org(org)})

    else:
        # which field was missing?
        fieldname = "name" if shortname else "shortname"

        return JSONResponse(
            {"error": f"Missing value for required field: { fieldname }", "org": None}
        )
