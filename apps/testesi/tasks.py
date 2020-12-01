from huey import RedisHuey
from huey import crontab
from django.conf import settings
from huey.contrib import djhuey as huey


@huey.periodic_task(crontab(minute='*/1'))
def testtask():
    print('This task runs every three minutes')
