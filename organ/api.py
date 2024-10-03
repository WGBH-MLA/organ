from fastapi import Depends
from fastcrud import crud_router

from organ.db import get_async_session
from organ.models import OpenVaultCatalog, Organization, OrganizationSchema
from organ.oauth import is_user_authenticated

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
    create_deps=[Depends(is_user_authenticated)],
    read_deps=None,
    read_multi_deps=[Depends(is_user_authenticated)],
    update_deps=[Depends(is_user_authenticated)],
    delete_deps=[Depends(is_user_authenticated)],
    db_delete_deps=[Depends(is_user_authenticated)],
)
