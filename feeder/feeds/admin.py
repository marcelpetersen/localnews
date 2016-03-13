from django.contrib import admin
from models import *
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.


class FeedsAdmin (admin.ModelAdmin):
	list_display = ('__unicode__', 'link', 'time', 'image', 'source')

	class Meta:
		model = Feeds

admin.site.register (Feeds, FeedsAdmin)
# admin.site.register(User)
admin.site.register(Exclude)
admin.site.register(Favorites)
# TokenAdmin.raw_id_fields = ('user',)