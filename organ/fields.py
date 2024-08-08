from dataclasses import dataclass

from starlette_admin.fields import BaseField


@dataclass
class ShowImageField(BaseField):
    display_template = "displays/show_image.html"
    render_function_key = "show_image"


@dataclass
class ShowOrgLogoField(BaseField):
    display_template = "displays/show_org_logo.html"
    render_function_key = "show_org_logo"
