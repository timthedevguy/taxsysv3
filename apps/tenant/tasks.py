from huey.contrib.djhuey import task, db_task
from ..testesi import testesi_client
from ..eveonline_esi import eveesi_client
from ..tenant.models import Corporation, Character
from datetime import datetime
from time import sleep
import sys
import logging
import os


@db_task()
def get_director_details(user, characters):
    character_info = {}
    corporations = []

    # Loop through all characters
    for character in characters:
        # Get Character info
        character_info[character] = testesi_client.get_character(character)
        if character_info[character]['corporation_id'] not in corporations:
            corporations.append(character_info[character]['corporation_id'])

    for corporation in corporations:
        # Check if Corporation is in DB
        if not Corporation.objects.filter(corporation_id=corporation).exists():
            # Get ESI info
            corporation_info = eveesi_client.get_corporation(corporation)['data']
            corp = Corporation(name=corporation_info['name'])
            corp.corporation_id = corporation
            corp.ceo_id = corporation_info['ceo_id']
            corp.save()

    for character_id in characters:
        if not Character.objects.filter(character_id=character_id).exists():
            char = Character(user_id=user.id)
            char.character_id = character_id
            char.name = character_info[character_id]['name']
            char.corporation = Corporation.objects.get(corporation_id=character_info[character_id]['corporation_id'])

            # Get Corp History
            history = eveesi_client.get_character_corporation_history(character_id)['data']
            if history[0]['corporation_id'] == character_info[character_id]['corporation_id']:
                # Current is correct
                char.join_date = datetime.strptime(history[0]['start_date'], '%Y-%m-%dT%H:%M:%SZ')
            else:
                # TODO Report an error here
                pass

            char.save()
