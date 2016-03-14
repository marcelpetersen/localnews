from rest_framework import serializers
from models import Feeds, Exclude, Favorites
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	exclude = serializers.PrimaryKeyRelatedField(many = True, read_only = True )
	favorites = serializers.PrimaryKeyRelatedField(many = True, queryset = Favorites.objects.all() )

	class Meta:
		model = User
		# read_only_fields = ('created_at', 'updated_at')
		fields = ('id', 'username', 'favorites','exclude')

		# def create(self, **validated_data):
		# 	return User.objects.create(**validated_data)

class FeedSerializer(serializers.ModelSerializer):

	class Meta: 
		model = Feeds
		fields = ('id', 'title', 'link', 'time', 'image', 'source')
		# read_only_fields = ('__all__')


class SourceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Feeds
		fields = ['source',]


class FavoriteSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source = 'user.username')

	class Meta:
		model = Favorites
		fields = ('id','user', 'title', 'link', 'time', 'image', 'source', 'fav_id')


class ExcludeSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source = 'user.username')

	class Meta:
		model = Exclude
		fields = ('source', 'user')