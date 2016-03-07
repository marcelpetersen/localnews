from rest_framework import serializers
from models import Feeds, Exclude, Favorites

class FeedSerializer(serializers.ModelSerializer):

	class Meta: 
		model = Feeds
		fields = '__all__'
		read_only_fields = ('__all__')


class SourceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Feeds
		fields = ['source',]


class FavoriteSerializer(serializers.ModelSerializer):

	class Meta:
		model = Favorites
		fields = '__all__'


class ExcludeSerializer(serializers.ModelSerializer):

	class Meta:
		model = Exclude
		fields = '__all__'