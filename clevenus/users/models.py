from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from datetime import datetime, time
import pytz

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length=256)
    date = models.DateField(null=True)
    time = models.TimeField(null=True, blank=True)
    datetime = models.DateTimeField(null=True)
    city = models.ForeignKey('charts.City', null=True)
    chart = models.ForeignKey('charts.Chart', related_name='profile', null=True)
    img = models.ImageField(null=True, blank=True)

    @classmethod
    def create(cls, user, date, time, city_name):
        self = UserProfile()
        self.user = user
        self.date = date
        self.time = time
        self.city_name = city_name
        self.save()
        return self

    def update_datetime_city(self):
        if self.date:
            if self.time:
                self.datetime = datetime.combine(self.date, self.time)
            else:
                self.datetime = datetime.combine(self.date, time(12, 0))

            if self.city:
                self.datetime = self.city.timezone.localize(self.datetime)
                self.lat = self.city.lat
                self.lng = self.city.lng
            else:
                self.datetime = pytz.utc.localize(self.datetime)


    def save(self, *args, **kwargs):
        from charts.models import Chart
        self.name = "%s %s" % (self.user.first_name, self.user.last_name)
        self.update_datetime_city()
        super(UserProfile, self).save(*args, **kwargs)
        if self.chart:
            self.chart.date = self.date
            self.chart.time = self.time
            self.chart.save()
        else:
            if self.date:
                self.chart = Chart.create(user=self.user.profile, name=self.name, date=self.date, time=self.time, city=self.city)
                self.chart.save()
        super(UserProfile, self).save(force_update=True)

    def __unicode__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)





def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


@classmethod
def user_create(cls, **kwargs):
    user = User()
    for k, v in kwargs.iteritems():
        if k == 'password':
            user.set_password(v)
        else:
            setattr(user, k, v)
    user.save()
    for k, v in kwargs.iteritems():
        setattr(user.profile, k, v)
    user.profile.save()
    return user


User.add_to_class('create', user_create)