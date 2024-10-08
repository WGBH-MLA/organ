from starlette_admin import URLField
from starlette_admin.contrib.sqlmodel import ModelView

from organ.fields import ShowImageField, ShowOrgLogoField


class OrganizationView(ModelView):
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


class OpenVaultCatalogView(ModelView):
    label = 'Open Vault Catalog'
