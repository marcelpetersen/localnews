from django.contrib import admin
from models import *
# Register your models here.


class FeedsAdmin (admin.ModelAdmin):
	list_display = ('__unicode__', 'link', 'time', 'image', 'source')

	class Meta:
		model = Feeds

admin.site.register (Feeds, FeedsAdmin)