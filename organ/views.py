# from typing import Any, Dict

# from jinja2 import Template
# from sqlalchemy import desc, func, select
# from sqlalchemy.orm import Session
# from starlette.requests import Request
# from starlette.responses import Response
# from starlette.templating import Jinja2Templates
from starlette_admin import URLField
from starlette_admin.contrib.sqlmodel import ModelView

# from starlette_admin.exceptions import FormValidationError
# # from app.sqla.fields import MarkdownField, CommentCounterField
# # from app.sqla.models import Comment, Post, User
from organ.fields import ShowImageField

# from starlette_admin.exceptions import FormValidationError


class OrganizationView(ModelView):
    # page_size_options = [5, 10, 25, -1]
    fields = [
        "uid",
        "name",
        "shortname",
        "state",
        URLField("url"),
        ShowImageField(
            "logo_url", label="Logo", display_template="displays/showimage.html"
        ),
        "about",
        "productions",
    ]

    # detail_template = "organization_detail.html"

    # Only show the counter on list view
    # exclude_fields_from_list = ["comments"]
    exclude_fields_from_create = ["uid"]
    exclude_fields_from_edit = ["uid"]
    # exclude_fields_from_detail = ["comments_counter"]
    # # Sort by full_name asc and username desc by default
    # fields_default_sort = ["full_name", (User.username, True)]

    # async def select2_selection(self, obj: Any, request: Request) -> str:
    #     template_str = "<span>{{obj.full_name}}</span>"
    #     return Template(template_str, autoescape=True).render(obj=obj)

    # def can_delete(self, request: Request) -> bool:
    #     return False
