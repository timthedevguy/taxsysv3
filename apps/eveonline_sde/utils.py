from django.db import models
from django.db import connection


class CustomFloatField(models.Field):
    def db_type(self, connection):
        return 'float'


def invtype_details(typeID: int) -> dict:
    """
    Something here
    :param typeID: TypeID of Item
    :return: Array of Details
    """
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
                '            WHERE "dgmTypeAttributes"."typeID" = %s' \
                '            AND "attributeID" = 790) as "refineSkill",' \
                '       (SELECT count("materialTypeID")' \
                '            FROM "invTypeMaterials"' \
                '            WHERE "invTypeMaterials"."typeID" = %s) AS "materialCount",' \
                '       (SELECT "invGroups"."groupName"' \
                '            FROM "invGroups"' \
                '            WHERE "invGroups"."groupID" = "invTypes"."groupID") as "groupName",' \
                '       (SELECT "invMarketGroups"."marketGroupName"' \
                '            FROM "invMarketGroups"' \
                '            WHERE "invMarketGroups"."marketGroupID" = "invTypes"."marketGroupID") as "marketGroupName"' \
                'FROM "invTypes"' \
                'WHERE "invTypes"."typeID" = %s'
        cursor.execute(query, [typeID, typeID, typeID])
        rows = dictfetchall(cursor)
        details = rows[0]

        query = 'SELECT "invTypeMaterials"."materialTypeID",' \
                '       "invTypeMaterials".quantity,' \
                '       iT."typeName"' \
                'FROM "invTypeMaterials"' \
                '         INNER JOIN "invTypes" iT ON "invTypeMaterials"."materialTypeID" = iT."typeID"' \
                'WHERE "invTypeMaterials"."typeID" = %s'

        cursor.execute(query, [typeID])
        rows = dictfetchall(cursor)

        details['materials'] = rows
        return details


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
