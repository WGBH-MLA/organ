import uuid
from typing import Any, Dict, List, Optional

from sqlmodel import Field, Relationship, SQLModel
from starlette.requests import Request


class Organization(SQLModel, table=True):
    __tablename__ = "organizations"
    id: Optional[int] = Field(default=None, primary_key=True)
    # create with new uuid
    uid: str = Field(index=True, default=uuid.uuid4(), unique=True)
    # name must be unique because even if there were two stations with identical names, they would still need to be differentiated somehow
    name: str = Field(index=True, unique=True)
    shortname: str = Field(index=True)
    state: Optional[str] = Field(index=True)
    url: Optional[str] = Field(index=True)
    logo_url: Optional[str] = Field(index=True)
    about: Optional[str] = Field(index=True)
    productions: Optional[str] = Field(index=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    # display name
    full_name: str = Field(min_length=3, index=True)
    # login name
    username: str = Field(index=True, unique=True)

    password: str = Field(index=False)

    async def __admin_repr__(self, request: Request):
        return self.full_name

    async def __admin_select2_repr__(self, request: Request) -> str:

        template_str = '<div class="d-flex align-items-center">{{obj.full_name}} <div>'
        return Template(template_str, autoescape=True).render(obj=self, url=url)


# class UserSession(SQLModel, table=True):
#   id: Optional[int] = Field(default=None, primary_key=True)
#   username: str
