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
	title = models.TextField(unique = True)
	link = models.TextField()
	time = models.DateTimeField()
	image = models.TextField(max_length=400)
	source = models.TextField (max_length=400)
	location = models.CharField(max_length=2)

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
	source = models.CharField(max_length = 255)

	def __unicode__(self):
		return self.source

class States (models.Model):
	user = models.ForeignKey(User, related_name = 'states')
	state = models.CharField(max_length=2)
	city = models.CharField(max_length= 200)

	def __unicode__(self):
		return self.state
	class Meta:
		ordering = ["-id"]

class Suggestions(models.Model):
	user = models.ForeignKey(User, related_name = 'suggester')
	name= models.CharField(max_length=255, blank = True)
	link = models.CharField(max_length=255, blank= True)
	location = models.CharField(max_length=255, blank= True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ["-id"]


class Email(models.Model):
	email = models.EmailField(max_length=254)
	subject = models.CharField(max_length=254)
	message = models.TextField()








