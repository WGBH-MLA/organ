from typing import Annotated
from uuid import UUID, uuid4

from pydantic import AnyHttpUrl, BeforeValidator, TypeAdapter
from sqlmodel import Field, SQLModel
from starlette.requests import Request

http_url_adapter = TypeAdapter(AnyHttpUrl)

Url = Annotated[
    str | None,
    BeforeValidator(lambda value: str(http_url_adapter.validate_python(value))),
]


class OrganizationSchema(SQLModel):
    name: str = Field(
        default=None, index=True, schema_extra={"validation_alias": "Name"}
    )
    shortname: str = Field(
        default=None, index=True, schema_extra={"validation_alias": "Short name"}
    )
    state: str | None = Field(
        default=None, index=True, schema_extra={"validation_alias": "State"}
    )
    url: Url = Field(default=None, index=True, schema_extra={"validation_alias": "Url"})
    logo_url: str | None = Field(
        default=None, index=True, schema_extra={"validation_alias": "Logo"}
    )
    about: str | None = Field(default=None, schema_extra={"validation_alias": "About"})
    productions: str | None = Field(
        default=None, index=True, schema_extra={"validation_alias": "Productions"}
    )
    latitude: float | None = Field(default=None, index=True)

    longitude: float | None = Field(default=None, index=True)

    ovid: str | None = Field(default=None, index=True)


class Organization(OrganizationSchema, table=True):
    __tablename__ = "organizations"
    id: int | None = Field(default=None, primary_key=True)
    uid: UUID = Field(index=True, default_factory=uuid4, unique=True)


class User(SQLModel, table=True):
    __tablename__ = "users"
    identity: str = Field(primary_key=True)
    name: str | None = Field(default=None, index=True)
    display_name: str | None = Field(default=None, index=True)
    avatar_url: str | None = Field(default=None, index=True)

    async def __admin_repr__(self, request: Request):
        return self.display_name
