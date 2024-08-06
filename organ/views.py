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
from organ.fields import ShowImageField, ShowOrgLogoField

# from starlette_admin.exceptions import FormValidationError


class OrganizationView(ModelView):
    # page_size_options = [5, 10, 25, -1]
    fields = [
        'id',
        'name',
        'shortname',
        'state',
        URLField('url'),
        ShowOrgLogoField(
            'logo_url', label='Logo', display_template="displays/show_org_logo.html"
        ),
        'latitude',
        'longitude',
        'about',
        'productions',
        'ovid',
        'uid',
    ]

    exclude_fields_from_create = ['uid']
    exclude_fields_from_edit = ['uid']


class UserView(ModelView):
    fields = [
        'identity',
        'name',
        'display_name',
        ShowImageField(
            'avatar_url', label='Avatar', display_template="displays/show_image.html"
        ),
    ]
