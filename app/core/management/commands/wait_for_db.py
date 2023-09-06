"""
    Django command to wait for the database to be availabe
    This command solves the Database race condition of the time waiting till the db is set up for working
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to wait for the database """

    def handle(self, *args, **options):
        """ Entrypoint for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailabe')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Databases available'))
