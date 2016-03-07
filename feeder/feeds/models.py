from django.db import models

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
	title = models.CharField(max_length = 255, unique = True)
	link = models.URLField(max_length = 255)
	time = models.DateTimeField()
	image = models.URLField(max_length = 255, blank = True)
	source = models.CharField (max_length = 255)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-time']


class Exclude(models.Model):
	source = models.CharField(max_length = 255, unique = True)

	def __unicode__(self):
		return self.source

