from django.shortcuts import render
from rest_framework import viewsets, generics
from serializers import FeedSerializer, SourceSerializer, FavoriteSerializer, ExcludeSerializer
from models import Feeds, Favorites, Exclude
# Create your views here.

class FeedViews(generics.ListCreateAPIView):
	# model = Feeds
	serializer_class = FeedSerializer
	exclude_list = Exclude.objects.values('source')




	def get_queryset(self):
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

class FavoriteUpdate(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = FavoriteSerializer
	queryset = Favorites.objects.all()


class ExcludeViewSet(generics.ListCreateAPIView):
	model = Exclude
	# lookup_field = 'source'
	serializer_class = ExcludeSerializer
	queryset = Exclude.objects.all()

class ExcludeDestroyViewSet(generics.RetrieveUpdateDestroyAPIView):
	# model = Exclude
	lookup_field = 'source'
	serializer_class = ExcludeSerializer
	queryset = Exclude.objects.all()

