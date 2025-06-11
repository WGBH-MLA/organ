from starlette_admin import URLField, action
from starlette_admin.contrib.sqlmodel import ModelView
from starlette_admin.exceptions import ActionFailed
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

    # This is to prevent the upload_csv action from being shown in the actions dropdown
    actions = ['delete']

    @action(
        name='upload_csv',
        text='Upload CSV',
        custom_response=True,
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
            if len(row) != 2:
                errors.append(
                    f"Invalid row {n}: {row}. Each row must contain exactly 2 columns."
                )
                continue
            if not row[0] or not row[1]:
                errors.append(f"Invalid row {n}: {row}. OVID and GUID cannot be empty.")
                continue
            if not row[1].startswith('cpb-aacip-'):
                errors.append(
                    f"Invalid row {n}: {row}. GUID must start with 'cpb-aacip-'."
                )
                continue
            ovid, guid = row[0], row[1]
            records.append({'ovid': ovid, 'guid': guid})

        if errors:
            log.error('Errors found while importing CSV file:', errors)
            raise ActionFailed(f"{len(errors)} errors importing csv file: {errors}")

        if not records:
            log.error('No valid records found in the CSV file.')
            raise ActionFailed("No valid records found in the CSV file.")

        records_dict = {record['ovid']: record['guid'] for record in records}

        from organ.models import OpenVaultCatalog
        from sqlmodel import select, Session
        from organ.db import engine

        with Session(engine) as db:
            existing_records = db.exec(
                select(OpenVaultCatalog).where(
                    OpenVaultCatalog.ovid.in_([record['ovid'] for record in records])
                )
            ).all()
            if existing_records:
                log.warning(
                    f"{len(existing_records)} records already exist in the database: {[r.ovid for r in  existing_records]}"
                )
                for existing_record in existing_records:
                    existing_record.guid = records_dict[existing_record.ovid]
                    db.add(existing_record)
                    del records_dict[existing_record.ovid]

            for ovid, guid in records_dict.items():
                new_record = OpenVaultCatalog(ovid=ovid, guid=guid)
                db.add(new_record)
            db.commit()

        log.success(f'{len(records)} records updated successfully!')
        return f"{len(records)} records updated successfully!"
