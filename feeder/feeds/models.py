from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.


class Feeds(models.Model):
	title = models.CharField(max_length = 255, unique = True)
	link = models.URLField(max_length = 255)
	time = models.DateTimeField()
	image = models.URLField(max_length = 255)
	source = models.CharField (max_length = 255)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-time']

class Favorites(models.Model):
	user = models.ForeignKey(User, related_name = 'favorites')
	fav_id = models.IntegerField()
	title = models.CharField(max_length = 255)
	link = models.URLField(max_length = 255)
	time = models.DateTimeField()
	image = models.URLField(max_length = 255, blank = True)
	source = models.CharField (max_length = 255)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-id']


class Exclude(models.Model):
	user = models.ForeignKey(User, related_name = 'exclude')
	source = models.CharField(max_length = 255, unique = True)

	def __unicode__(self):
		return self.source

