from fastcrud import crud_router

from organ.db import get_async_session
from organ.models import Organization, OrganizationSchema

orgs = crud_router(
    model=Organization,
    session=get_async_session,
    path='/orgs',
    tags=['orgs'],
    create_schema=OrganizationSchema,
    update_schema=OrganizationSchema,
)

# users = crud_router(User)
