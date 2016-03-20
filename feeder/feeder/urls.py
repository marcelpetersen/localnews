from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken import views
from feeds.views import *

router = routers.SimpleRouter()
# router.register (r'destroy', ExcludeDestroyViewSet)

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ap/', include(router.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^api/feeds/$', FeedViews.as_view(), name = 'feeds'),
    url(r'^api/feeds/source/$', FeedSource.as_view(), name = 'feed_source'),
    url(r'^api/feeds/favorite/$', FavoriteViews.as_view(), name = 'feed_source'),
    url(r'^api/feeds/updatefavorite/(?P<pk>[0-9]+)$', FavoriteUpdate.as_view(), name = 'feed_source'),
    url(r'^api/feeds/exclude/$', ExcludeViewSet.as_view(), name = 'feed_exclude'),
	url(r'^api/feeds/destroy/(?P<source>.+)$', ExcludeDestroyViewSet.as_view(), name = 'destroy'),
    url(r'^api/feeds/users/$', UserViews.as_view(), name = 'user'),
    url(r'^api/feeds/userupdate/(?P<pk>[0-9]+)$', UserUpdate.as_view(), name = 'userupdate'),
    url(r'^api/feeds/state/$', StateView.as_view(), name = 'state'),
    url(r'^api/feeds/stateupdate/(?P<pk>[0-9]+)$', StateUpdate.as_view(), name = 'stateupdate'),
    url(r'^api/feeds/city/$', City.as_view(), name = 'city'),
    url(r'^api/feeds/suggest/$', SuggestView.as_view(), name = 'suggestion'),


]
