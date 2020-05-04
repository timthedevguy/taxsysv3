import requests
import bz2
import subprocess
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.eveonline import esi
from apps.eveonline import market
from django.db import connection
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Date Test Commmand'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        today = timezone.now()
        print('Today is: {today}'.format(today=today))
        yesterday = today - timedelta(days=1)
        print('Yesterday was: {yesterday}'.format(yesterday=yesterday))
