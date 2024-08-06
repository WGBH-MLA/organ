from dataclasses import dataclass

from starlette_admin.fields import BaseField


@dataclass
class ShowImageField(BaseField):
    display_template = "displays/show_image.html"
    render_function_key = "show_image"
    # async def parse_obj(self, request: Request, obj: Any) -> Any:
    #   return f"<img src='{ obj.logo_url }' class='logo-image' />"


@dataclass
class ShowOrgLogoField(BaseField):
    display_template = "displays/show_org_logo.html"
    render_function_key = "show_org_logo"
