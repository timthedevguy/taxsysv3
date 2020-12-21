from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class Command(BaseCommand):
    help = 'Date Test Commmand'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # today = timezone.now()
        # print('Today is: {today}'.format(today=today))
        # yesterday = today - timedelta(days=1)
        # print('Yesterday was: {yesterday}'.format(yesterday=yesterday))
        for app in settings.INSTALLED_APPS:
            if app.startswith('apps.eveonline_sde.'):
                print(app)
