from huey.contrib.djhuey import task
from time import sleep
import sys
import logging
import os

logger = logging.getLogger(__name__)


@task(retries=0)
def test_task():
    logger.critical('Task Started')
    sleep(5)
    logger.critical('Task Completed')
