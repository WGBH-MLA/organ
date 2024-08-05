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
    # create with new uuid
    uid: UUID = Field(index=True, default_factory=uuid4, unique=True)


class User(SQLModel, table=True):
    # id: int | None = Field(primary_key=True)
    identity: str = Field(primary_key=True)
    # display name
    name: str | None = Field(default=None, index=True)
    display_name: str | None = Field(default=None, index=True)
    avatar_url: str | None = Field(default=None, index=True)
    # full_name: str = Field(min_length=3, index=True)
    # login name
    # username: str = Field(index=True, unique=True)

    # password: str = Field(index=False)

    async def __admin_repr__(self, request: Request):
        return self.display_name

    # async def __admin_select2_repr__(self, request: Request) -> str:

    #     template_str = (
    #         '<div class="d-flex align-items-center">{{obj.display_name}} <div>'
    #     )
    # return Template(template_str, autoescape=True).render(obj=self, url=url)


# class UserSession(SQLModel, table=True):
#   id: Optional[int] = Field(default=None, primary_key=True)
#   username: str
