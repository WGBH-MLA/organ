from starlette_admin import URLField, action
from starlette_admin.contrib.sqlmodel import ModelView
from loguru import logger as log
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
    list_template = 'ov_catalog.html'
    actions = ['upload_csv']

    @action(
        name='upload_csv',
        text='Upload CSV',
        confirmation='''
            Please make sure the CSV file is formatted correctly before uploading:
                                                    <ul>
                                                        <li>Column 1: OVID</li>
                                                        <li>Column 2: GUID</li>
                                                    </ul>
        ''',
        form='''<form id="modal-form" name="upload_csv" method="POST" enctype="multipart/form-data">
                                            <input type="file" name="csv_file" accept=".csv" required>
                                        </form>''',
    )
    async def upload_csv(self, request, pks):
        form = await request.form()
        csv_file = form.get('csv_file')
        if not csv_file:
            return {"error": "No file uploaded"}, 400
        # Process the CSV file
        import csv
        from io import StringIO

        csv_content = await csv_file.read()
        await csv_file.seek(0)
        file_string = StringIO(csv_content.decode('utf-8').replace('\r', '\n'))
        csv_reader = csv.reader(file_string)
        records = []
        errors = []
        for n, row in enumerate(csv_reader):
            if len(row) < 2:
                errors.append(
                    f"Invalid row {n}: {row}. Each row must contain at least 2 columns."
                )
                continue
            ovid, guid = row[0], row[1]
            records.append({'ovid': ovid, 'guid': guid})

        if errors:
            log.error('Errors found while importing CSV file:', errors)
            return f"{len(errors)} errors importing csv file"

        log.success(f'{len(records)} records uploaded successfully!')
        return f"{len(records)} records uploaded successfully!"
