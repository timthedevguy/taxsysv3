import requests
import bz2
import subprocess
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = 'Updates SDE from Fuzzworks'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for table in settings.EVEONLINE_SDE_TABLES:
            self.stdout.write(self.style.NOTICE('Updating {table}...'.format(table=table)))
            # Download the file
            r = requests.get('https://www.fuzzwork.co.uk/dump/latest/{table}.csv.bz2'.format(table=table))
            open('{table}.csv.bz2'.format(table=table), 'wb').write(r.content)

            # Extract the SQL Dump
            zipfile = bz2.BZ2File('{table}.csv.bz2'.format(table=table))
            data = zipfile.read()
            newfilepath = '{table}.csv'.format(table=table)
            open(newfilepath, 'wb').write(data)

            # Create passfile
            with open('passfile', 'w') as f:
                f.write('{hostname}:{port}:{database}:{username}:{password}'.format(
                    hostname=settings.DATABASES['default']['HOST'],
                    port=5432,
                    database=settings.DATABASES['default']['NAME'],
                    username=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD']
                ))

            # Import the SQL Dump
            p = subprocess.run('psql --host=10.0.1.13 --username=postgres --dbname=taxsys --command="\\copy invTypes FROM \'invTypes.csv\' delimiter \',\' csv header"'.format(
                table=table
            ), env={'PGPASSFILE': 'passfile'})

            # with connection.cursor() as cursor:
            #     cursor.execute("copy invTypes FROM \'invTypes.csv\' delimiter \',\' csv header")

            #shell=True, , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            print(p)

            # Delete the files
            # os.remove('{table}.sql.bz2'.format(table=table))
            # os.remove('{table}.sql'.format(table=table))
