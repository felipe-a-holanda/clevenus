from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from charts.models import Chart, City
from datetime import datetime
from django.contrib.auth.models import User
import csv
from django.utils.text import slugify
import traceback

class Command(BaseCommand):
    help = 'Populate initial astro data'

    def read_csv(self, path):
        rows = []
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
        return rows

    @transaction.atomic
    def create_user(self, r):
        city = None
        for k, v in r.iteritems():
            if k=='date':
                r[k] = datetime.strptime(v, '%Y/%m/%d').date()
            if k=='time':
                if v:
                    r[k] = datetime.strptime(v, '%H:%M:%S').time()
                else:
                    r[k] = None
            if k=='city_name':
                city = City.create(v)
        if city:
            r['city'] = city
        r['username'] = slugify(r['name'])
        try:
            r['first_name'], r['last_name'] = r['name'].split(' ',1)
        except:
            r['first_name'] = r['name']

        u = User.create(**r)
        u.save()
        #try:
        #    u = User.create(**r)
        #    u.save()
        #except Exception as e:
        #    print 'error:', r['name'], e
        #else:
        #    print 'user created:', r['name']
        return u

    def create_users(self):
        rows = self.read_csv('data/users.csv')
        for r in rows:

            #u = self.create_user(r)
            #print u
            try:
                u = self.create_user(r)
            except Exception as e:

                print('error', r['name'], e)
                print(traceback.format_exc())
            else:
                print(u)


    @transaction.atomic()
    def create_sys_charts(self):
        from datetime import datetime
        from charts.models import Chart
        from django.contrib.auth.models import User
        admin = User.objects.get(username='admin')
        now = datetime.now()
        chart = Chart.create(admin.profile, 'Now', now.date(), now.time())
        chart.save()



    def handle(self, *args, **options):
        #self.create_sys_charts()
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
