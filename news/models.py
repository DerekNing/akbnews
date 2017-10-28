from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Account(models.Model):

    user = models.OneToOneField(User)
    karma = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

class Link(models.Model):

    url = models.URLField()
    title = models.CharField(max_length=128)
    creator = models.ForeignKey(Account, related_name='creator', on_delete=models.CASCADE)
    voters = models.ManyToManyField(Account, related_name='voters', through='Vote')
    score = models.IntegerField(default=0)
    post_time = models.DateTimeField(default=timezone.now, blank=True)
    view = models.IntegerField(default=0)
    hot = models.FloatField()

    def __unicode__(self):
        return self.title

class Vote(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    up = models.IntegerField(default=0)

    def __unicode__(self):
        return self.account.user.username + ': ' + self.link.title
