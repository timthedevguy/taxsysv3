import requests
import bz2
import subprocess
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Updates SDE from Fuzzworks'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Downloading Postgres dump of Eve SDE...'))

        # Download the dump
        r = requests.get('https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2')
        open('postgres-latest.dmp.bz2', 'wb').write(r.content)

        # Extract the dump
        self.stdout.write(self.style.NOTICE('Extracting Postgres dump of Eve SDE...'))
        zipfile = bz2.BZ2File('postgres-latest.dmp.bz2')
        data = zipfile.read()
        postgres_dmp = 'postgres-latest.dmp'
        open(postgres_dmp, 'wb').write(data)
        zipfile.close()

        for table in settings.EVEONLINE_SDE_TABLES:
            # Create Commands
            drop_command = 'psql -h {host} -U {user} -p 5432 -w -d {database} -q -c "drop table \\"{table}\\""'.format(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                database=settings.DATABASES['default']['NAME'],
                table=table
            )
            import_command = 'pg_restore -h {host} -U {user} -p 5432 -w -d {database} -t {table} -O postgres-latest.dmp'.format(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                database=settings.DATABASES['default']['NAME'],
                table=table
            )

            if os.name == 'nt':
                self.stdout.write(self.style.NOTICE('Droping {table}...'.format(table=table)))
                p = subprocess.run(drop_command, shell=False)
                self.stdout.write(self.style.NOTICE('Importing {table}...'.format(table=table)))
                subprocess.run(import_command, shell=False)
            else:
                self.stdout.write(self.style.NOTICE('Droping {table}...'.format(table=table)))
                subprocess.run(drop_command, shell=True, env={
                    'PGPASSWORD': settings.DATABASES['default']['PASSWORD']
                })
                self.stdout.write(self.style.NOTICE('Importing {table}...'.format(table=table)))
                subprocess.run(import_command, shell=True, env={
                    'PGPASSWORD': settings.DATABASES['default']['PASSWORD']
                })

        # Delete the files
        os.remove('postgres-latest.dmp.bz2'.format(table=table))
        os.remove('postgres-latest.dmp'.format(table=table))
