from django.shortcuts import render
from django.http import request, HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions, status
from serializers import *
from models import *
from rest_framework.response import Response

# Create your views here.

class FeedViews(generics.ListCreateAPIView):
	
	serializer_class = FeedSerializer
	
	def get_queryset(self):
		if self.request.user.is_authenticated():
			user = self.request.user
			exclude_list = Exclude.objects.filter(user=user).values('source')
			location_list = States.objects.filter(user=user).values('state')
		else:
			exclude_list = []
			location_list = []

		return Feeds.objects.filter(location__in=location_list).exclude(source__in=exclude_list)

class FeedSource (generics.ListAPIView):
	serializer_class = SourceSerializer
	def get_queryset(self):
		user = self.request.user
		location_list = States.objects.filter(user=user).values('state')
		return Feeds.objects.filter(location__in=location_list).values('source').order_by('source').distinct()


class FavoriteViews(generics.ListCreateAPIView):
	serializer_class = FavoriteSerializer

	def get_queryset(self):

		user = self.request.user
		return Favorites.objects.filter(user=user)

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

class FavoriteUpdate(generics.RetrieveUpdateDestroyAPIView):
	# lookup_field = 'fav_id'
	serializer_class = FavoriteSerializer
	queryset = Favorites.objects.all()


class ExcludeViewSet(generics.ListCreateAPIView):
	model = Exclude
	# lookup_field = 'source'
	serializer_class = ExcludeSerializer
	# queryset = Exclude.objects.all()
	
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

	def get_queryset (self):
		user = self.request.user
		return Exclude.objects.filter(user=user)



class ExcludeDestroyViewSet(generics.RetrieveUpdateDestroyAPIView):
	# model = Exclude
	lookup_field = 'source'
	serializer_class = ExcludeSerializer
	
	def get_queryset (self):
		user = self.request.user
		return Exclude.objects.filter(user=user)

class StateView(generics.ListCreateAPIView):
	serializer_class = StateSerializer
	queryset = States.objects.all()

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

class StateUpdate(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = StateSerializer

	def get_queryset(self):
		user = self.request.user
		return States.objects.all()

class City(generics.ListCreateAPIView):
	serializer_class = StateSerializer

	def get_queryset(self):
		user = self.request.user
		return States.objects.filter(user=user)

class UserViews(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	
class UserUpdate (generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializers_class = UserSerializer

class SuggestView(generics.ListCreateAPIView):
	queryset = Suggestions.objects.all()
	serializer_class = SuggestSerializer
	
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

class EmailView(generics.ListCreateAPIView):
	queryset = Email.objects.all()
	serializer_class = EmailSerializer

def mainview(request):
	return render(request, "index.html")


