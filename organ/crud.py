from fastcrud import crud_router

from organ.db import get_async_session
from organ.models import OpenVaultCatalog, Organization, OrganizationSchema

orgs = crud_router(
    model=Organization,
    session=get_async_session,
    path='/orgs',
    tags=['orgs'],
    create_schema=OrganizationSchema,
    update_schema=OrganizationSchema,
)

ov_catalog = crud_router(
    model=OpenVaultCatalog,
    session=get_async_session,
    path='/ov',
    tags=['ov'],
    create_schema=OpenVaultCatalog,
    update_schema=OpenVaultCatalog,
)
