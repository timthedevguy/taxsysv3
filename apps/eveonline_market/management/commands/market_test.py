from django.core.management.base import BaseCommand
from django.conf import settings
from apps.eveonline_esi import eveesi_client
from apps.eveonline_market import market
from django.db import connection
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Market Test Commmand'

    def add_arguments(self, parser):
        parser.add_argument('type_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Pulling data for {}'.format(options['type_id'])))
        raw = eveesi_client.get_markets_region_orders(settings.MARKET_REGION, order_type='sell', type_id=options['type_id'],
                                            all=True)['data']
        if raw:
            jita = market.filter_by(raw, 'location_id', settings.MARKET_SYSTEM)
            print(market.pandas_stats(jita))
        else:
            print('Data returned is empty!')
        with connection.cursor() as cursor:
            query = 'SELECT "invTypes"."typeID",' \
                    '       "invTypes"."typeName",' \
                    '       "invTypes"."groupID",' \
                    '       "invTypes"."portionSize",' \
                    '       "invTypes"."marketGroupID",' \
                    '       (SELECT CASE' \
                    '            WHEN "valueInt" IS NULL THEN "valueFloat"' \
                    '            ELSE "valueInt" END' \
                    '            FROM "dgmTypeAttributes"' \
                    '            WHERE "dgmTypeAttributes"."typeID" = 19' \
                    '            AND "attributeID" = 790) as "refineSkill",' \
                    '       (SELECT count("materialTypeID")' \
                    '            FROM "invTypeMaterials"' \
                    '            WHERE "invTypeMaterials"."typeID" = 19) AS "materialCount",' \
                    '       (SELECT "invGroups"."groupName"' \
                    '            FROM "invGroups"' \
                    '            WHERE "invGroups"."groupID" = "invTypes"."groupID") as "groupName",' \
                    '       (SELECT "invMarketGroups"."marketGroupName"' \
                    '            FROM "invMarketGroups"' \
                    '            WHERE "invMarketGroups"."marketGroupID" = "invTypes"."marketGroupID") as "marketGroupName"' \
                    'FROM "invTypes"' \
                    'WHERE "invTypes"."typeID" = 19'
            cursor.execute(query, [19, 19, 1, 19])
            rows = dictfetchall(cursor)
            details = rows[0]

            query = 'SELECT "invTypeMaterials"."materialTypeID",' \
                    '       "invTypeMaterials".quantity,' \
                    '       iT."typeName",' \
                    '       t.tax,' \
                    '       t.id  AS "overrideID",' \
                    '       em.id AS "marketdataID",' \
                    '       em."weightedAverage",' \
                    '       em.max,' \
                    '       em.min,' \
                    '       em.median,' \
                    '       em.stddev,' \
                    '       em.percentile ' \
                    'FROM "invTypeMaterials"' \
                    '         INNER JOIN "invTypes" iT ON "invTypeMaterials"."materialTypeID" = iT."typeID"' \
                    '         LEFT JOIN tenant_override t ON "invTypeMaterials"."materialTypeID" = t."typeID" AND ' \
                    ' t."tenantID" = %s' \
                    '         LEFT JOIN eveonline_marketdata em ON "invTypeMaterials"."materialTypeID" = em."typeID" ' \
                    'AND em.date = %s ' \
                    'WHERE "invTypeMaterials"."typeID" = %s'

            cursor.execute(query, [1, (timezone.now() - timedelta(days=1)).date(), 19])
            rows = dictfetchall(cursor)

            details['materials'] = rows

        print(details)


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
