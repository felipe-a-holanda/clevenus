from django.core.management.base import BaseCommand
import csv
#import unicodecsv as csv
from django.contrib.auth.models import User
from charts.models import Event
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populate initial astro data'

    def parse_file(self, user):
        with open('data/users.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                print(row['city_name'])
                city_name = row['city_name']
                event_date = datetime.strptime(row['date'], '%Y/%m/%d').date()
                try:
                    event_time = datetime.strptime(row['time'], '%H:%M:%S').time()
                except:
                    event_time = None
                print(name, event_date)
                user.profile.add_event(name, city_name, event_date, event_time)

    def handle(self, *args, **options):
        User.objects.filter(is_superuser=False).delete()
        u = User.create(username='flp9001', email='flp9001@gmail.com', first_name='Felipe', last_name='Holanda', date=date(1986, 12, 22), time=time(6, 34), city_name='Limoeiro do Norte')
        self.parse_file(u)