from typing import Any

from starlette.requests import Request
from starlette_admin.fields import BaseField

from starlette_admin.fields import BaseField


class ShowImageField(BaseField):
    render_function_key: "show_image"
    # async def parse_obj(self, request: Request, obj: Any) -> Any:
    #   return f"<img src='{ obj.logo_url }' class='logo-image' />"
