import requests
import bz2
import subprocess
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.testesi import testesi_client
from apps.testauth.models import TestUser
from huey import crontab
from huey.contrib.djhuey import periodic_task, task


class Command(BaseCommand):
    help = 'Get Characters'

    def add_arguments(self, parser):
        parser.add_argument('character_id', nargs='+', type=int)

    def handle(self, *args, **options):
        user = TestUser.objects.get(auth_id=62118)
        result = testesi_client.get(settings.TESTESI_GET_CHARACTERS, testesi_client.get_access_token(), subject=user.subject)
        print(result)