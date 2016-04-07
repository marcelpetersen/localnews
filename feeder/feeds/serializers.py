from rest_framework import serializers
from models import Feeds, Exclude, Favorites, States, Suggestions, Email
from django.contrib.auth.models import User
from django.http import request, HttpResponse


class UserSerializer(serializers.ModelSerializer):
	exclude = serializers.PrimaryKeyRelatedField(many = True, read_only = True )
	favorites = serializers.PrimaryKeyRelatedField(many = True, queryset = Favorites.objects.all() )
	states = serializers.PrimaryKeyRelatedField(many= True, read_only = True)
	suggester = serializers.PrimaryKeyRelatedField(many= True, read_only = True)

	class Meta:
		model = User
		# read_only_fields = ('created_at', 'updated_at')
		fields = ('id', 'username', 'favorites','exclude', 'states', 'suggester')

		# def create(self, **validated_data):
		# 	return User.objects.create(**validated_data)

class FeedSerializer(serializers.ModelSerializer):

	class Meta: 
		model = Feeds
		fields = ('id', 'title', 'link', 'time', 'image', 'source', 'location')
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


class StateSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source = 'user.username')

	class Meta:
		model = States
		fields = ('id','state', 'user', 'city')

class SuggestSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source = 'user.username')

	class Meta:
		model = Suggestions
		fields = ('id', 'name', 'user', 'link', 'location')


class EmailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Email
		fields = ('__all__')



