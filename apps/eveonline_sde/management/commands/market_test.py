import requests
import bz2
import subprocess
import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.utils import timezone
from datetime import timedelta
from apps.eveonline_sde.utils import invtype_details


class Command(BaseCommand):
    help = 'Market Test Commmand'

    def add_arguments(self, parser):
        parser.add_argument('type_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Pulling data for {}'.format(options['type_id'])))
        print(invtype_details(options['type_id']))
