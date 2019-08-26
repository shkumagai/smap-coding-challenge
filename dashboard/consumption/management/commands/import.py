import csv
import os
import os.path
import sys
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import get_default_timezone

from consumption.models import Consumption, User


# Environment variables for one-time use
data_root = '..'
user_data_csv = os.path.join(data_root, 'data/user_data.csv')
consumption_data_root = os.path.join(data_root, 'data/consumption/')


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        users = []
        # Step 1: import users
        with open(user_data_csv, 'r') as fp_user:
            fp_user.readline()  # skip first row as column title
            user_reader = csv.DictReader(
                fp_user,
                fieldnames=(
                    'id',
                    'area',
                    'tariff',
                ),
            )
            for row in user_reader:
                user = User(
                    id=int(row['id']),
                    area=row['area'],
                    tariff=row['tariff'],
                )
                users.append(user)
            User.objects.bulk_create(users)
        sys.stderr.write(f'Total user data: {len(users):,} loaded.\n')

        # Step 2: import consumption data by each user
        total = 0
        for user in sorted(users, key=lambda u: u.id):
            consumption_csv_file_name = os.path.join(
                consumption_data_root,
                f'{user.id}.csv',
            )
            with open(consumption_csv_file_name, 'r') as fp_consumption:
                fp_consumption.readline()  # skip first row as column title

                consumptions = []
                consumption_reader = csv.DictReader(
                    fp_consumption,
                    fieldnames=(
                        'datetime',
                        'consumption',
                    ),
                )
                for row in consumption_reader:
                    consumption = Consumption()
                    # convert naive datetime value to timezone aware stuff
                    consumption.datetime = datetime.strptime(
                        row['datetime'],
                        '%Y-%m-%d %H:%M:%S',
                    ).astimezone(get_default_timezone())  # use UTC
                    consumption.consumption = float(row['consumption'])
                    consumption.user = user
                    consumptions.append(consumption)
                Consumption.objects.bulk_create(consumptions)

            sys.stderr.write(
                f'User id:{user.id} | '
                f'Consumption file: {consumption_csv_file_name} | '
                f'Loaded entry count: {len(consumptions)}'
                '\n',
            )
            total += len(consumptions)
        sys.stderr.write(f'Total consumption data: {total:,} loaded.\n')
