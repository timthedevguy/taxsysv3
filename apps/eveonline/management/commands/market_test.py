import requests
import bz2
import subprocess
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.eveonline import esi
from apps.eveonline import market


class Command(BaseCommand):
    help = 'Market Test Commmand'

    def add_arguments(self, parser):
        parser.add_argument('type_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Pulling data for {}'.format(options['type_id'])))
        raw = esi.get_markets_region_orders(settings.MARKET_REGION, order_type='sell', type_id=options['type_id'],
                                            all=True)['data']
        if raw:
            jita = market.filter_by(raw, 'location_id', settings.MARKET_SYSTEM)
            print(market.pandas_stats(jita))
            print(market.five_percent(jita))
        else:
            print('Data returned is empty!')
