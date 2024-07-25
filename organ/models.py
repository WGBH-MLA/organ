from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel
from starlette.requests import Request


class OrganizationSchema(SQLModel):
    name: str = Field(
        default=None, index=True, unique=True, schema_extra={"validation_alias": "Name"}
    )
    shortname: str = Field(
        default=None, index=True, schema_extra={"validation_alias": "Short Name"}
    )
    state: Optional[str] = Field(
        default=None, index=True, schema_extra={"validation_alias": "State"}
    )
    url: Optional[str] = Field(
        default=None, index=True, schema_extra={"validation_alias": "Url"}
    )
    logo_url: Optional[str] = Field(
        default=None, index=True, schema_extra={"validation_alias": "Logo Url"}
    )
    about: Optional[str] = Field(
        default=None, index=True, schema_extra={"validation_alias": "About"}
    )
    productions: Optional[str] = Field(
        default=None, index=True, schema_extra={"validation_alias": "Productions"}
    )
    location: Optional[str] = Field(default=None, index=True)


class Organization(OrganizationSchema, table=True):
    __tablename__ = "organizations"
    id: Optional[int] = Field(default=None, primary_key=True)
    # create with new uuid
    uid: UUID = Field(index=True, default_factory=uuid4, unique=True)


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
        # return Template(template_str, autoescape=True).render(obj=self, url=url)


# class UserSession(SQLModel, table=True):
#   id: Optional[int] = Field(default=None, primary_key=True)
#   username: str
