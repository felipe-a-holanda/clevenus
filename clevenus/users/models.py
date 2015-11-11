from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import hashlib
from datetime import datetime, time
import pytz



from allauth.account.signals import user_signed_up


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    username = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    birth = models.OneToOneField('charts.Event', related_name='birth_user', null=True)
    events = models.ManyToManyField('charts.Event', related_name='event_user')

    def get_absolute_url(self):
        return reverse('userprofile-view', args=[self.pk])



    @classmethod
    def create(cls, user, date, time, city_name):
        from charts.models import Event
        self = UserProfile()
        self.user = user
        self.username = user.username
        self.name = "%s %s" % (self.user.first_name, self.user.last_name)
        self.birth = Event.create(self.name, city_name, date, time)

        self.save()
        return self

    def add_event(self, name, city_name, date, time):
        from charts.models import Event
        event = Event.create(name, city_name, date, time)
        self.events.add(event)

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

    def profile_image_url(self, size=40):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        if len(fb_uid):
            return "http://graph.facebook.com/{uid}/picture?width={size}&height={size}".format(uid=fb_uid[0].uid, size=size)

        return "http://www.gravatar.com/avatar/{md5}?s={size}".format(md5=hashlib.md5(self.user.email.encode('utf-8')).hexdigest(), size=size)


    def save(self, *args, **kwargs):
        from charts.models import Chart
        self.name = "%s %s" % (self.user.first_name, self.user.last_name)
        #self.update_datetime_city()
        super(UserProfile, self).save(*args, **kwargs)
        #if self.chart:
        #    self.chart.date = self.date
        #    self.chart.time = self.time
        #    self.chart.save()
        #else:
            #if self.date:
                #self.chart = Chart.create(name=self.name, date=self.date, time=self.time, city=self.city)
                #self.chart.save()
        #super(UserProfile, self).save(force_update=True)

    def __str__(self):
        print("str of userprofile")
        return self.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __lt__(self, other):
        return self.name < other.name



@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        print(sociallogin)


from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


def create_user_profile(sender, instance, created, **kwargs):
    if created:

        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


@classmethod
def user_create(cls, **kwargs):
    from charts.models import Event
    user = User()
    for k, v in kwargs.items():
        if k == 'password':
            user.set_password(v)
        else:
            setattr(user, k, v)
    user.save()

    for k, v in kwargs.items():
        setattr(user.profile, k, v)




    user.profile.save()


    name = user.profile.name
    city_name = kwargs['city_name']
    event_date = kwargs['date']
    event_time = kwargs['time']
    birth = Event.create(name, city_name, event_date, event_time)

    user.profile.birth = birth
    user.profile.save()


    return user


User.add_to_class('create', user_create)