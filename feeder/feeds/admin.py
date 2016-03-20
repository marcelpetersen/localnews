from django.contrib import admin
from models import *
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.


class FeedsAdmin (admin.ModelAdmin):
	list_display = ('__unicode__', 'link', 'time', 'image', 'source')

	class Meta:
		model = Feeds

class StateAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'user', 'city')

	class Meta:
		model = States

class SuggestAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'link', 'location')

	class Meta:
		model = Suggestions

class ExcludeAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'user')

	class Meta:
		model = Exclude


admin.site.register (Feeds, FeedsAdmin)
admin.site.register(Exclude, ExcludeAdmin)
admin.site.register(Favorites)
admin.site.register(States, StateAdmin)
admin.site.register(Suggestions, SuggestAdmin)

# TokenAdmin.raw_id_fields = ('user',)