from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from charts.models import Chart, City
from datetime import datetime
from django.contrib.auth.models import User
import csv


class Command(BaseCommand):
    help = 'Populate initial astro data'

    def read_csv(self, path):
        rows = []
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
        return rows

    def create_users(self):
        rows = self.read_csv('data/users.csv')
        for r in rows:
            print r
            city = None
            for k, v in r.iteritems():
                if k=='date':
                    r[k] = datetime.strptime(v, '%Y-%m-%d').date()
                if k=='time':
                    r[k] = datetime.strptime(v, '%H:%M:%S').time()
                if k=='city_name':
                    city = City.create(v)
            if city:
                r['city'] = city
            u = User.create(**r)
            u.save()

    def create_sys_charts(self):
        from datetime import datetime
        from charts.models import Chart
        from django.contrib.auth.models import User
        admin = User.objects.get(username='admin')
        now = datetime.now()
        chart = Chart.create(admin.profile, 'Now', now.date(), now.time())
        chart.save()


    @transaction.atomic
    def handle(self, *args, **options):
        self.create_sys_charts()
        self.create_users()

    def x(self):
        c = City(name='Limoeiro do Norte')
        c.save()


        name = 'Felipe Andrade Holanda'
        d = datetime(1986, 12, 22, 6, 34)
        date = d.date()
        time = d.time()

        city = c
        chart = Chart(name=name, date=date, time=time, city=city)
        chart.save()
