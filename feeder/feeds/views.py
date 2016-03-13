from django.shortcuts import render
from django.http import request, HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions, status
from serializers import FeedSerializer, SourceSerializer, FavoriteSerializer, ExcludeSerializer, UserSerializer
from models import Feeds, Favorites, Exclude
from rest_framework.response import Response

# Create your views here.

class FeedViews(generics.ListCreateAPIView):
	# model = Feeds
	
	serializer_class = FeedSerializer
	exclude_list = Exclude.objects.values('source')


	def get_queryset(self):
		# user = self.request.user
		
		return Feeds.objects.exclude(source__in=self.exclude_list)


	def put(self, something):
		self.exclude_list.append(something)
		return 

class FeedSource (generics.ListAPIView):
	serializer_class = SourceSerializer
	queryset = Feeds.objects.values('source').order_by('source').distinct()


class FavoriteViews(generics.ListCreateAPIView):
	serializer_class = FavoriteSerializer
	queryset = Favorites.objects.all()

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

class FavoriteUpdate(generics.RetrieveUpdateDestroyAPIView):
	# lookup_field = 'pk'
	serializer_class = FavoriteSerializer
	queryset = Favorites.objects.all()


class ExcludeViewSet(generics.ListCreateAPIView):
	model = Exclude
	# lookup_field = 'source'
	serializer_class = ExcludeSerializer
	queryset = Exclude.objects.all()
	
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)


class ExcludeDestroyViewSet(generics.RetrieveUpdateDestroyAPIView):
	# model = Exclude
	lookup_field = 'source'
	serializer_class = ExcludeSerializer
	queryset = Exclude.objects.all()

class UserViews(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	# def get_permissions(self):
	# 	if self.request.method in permissions.SAFE_METHODS:
	# 		return (permissions.AllowAny(),)

	# 	if self.request.method == 'POST':
	# 		return (permissions.AllowAny(),)

	# 	return (permissions.IsAuthenticated(), IsAccountOwner(),)

	# def create(self, request):
	# 	serializer = self.serializer_class(data=request.data)

	# 	if serializer.is_valid():
	# 		User.objects.create_user(**serializer.validated_data)

	# 		return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

	# 	return Response({
	# 	'status': 'Bad request',
	# 	'message': 'Account could not be created with received data.'
	# 	}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdate (generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializers_class = UserSerializer

