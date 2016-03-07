from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from feeds.views import FeedViews, FeedSource, ExcludeViewSet, FavoriteViews, FavoriteUpdate, ExcludeDestroyViewSet

router = routers.SimpleRouter()
# router.register (r'destroy', ExcludeDestroyViewSet)

urlpatterns = [

    # Examples:
    # url(r'^$', 'feeder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ap/', include(router.urls)),
    
    url(r'^api/feeds/$', FeedViews.as_view(), name = 'feeds'),
    url(r'^api/feeds/source/$', FeedSource.as_view(), name = 'feed_source'),
    url(r'^api/feeds/favorite/$', FavoriteViews.as_view(), name = 'feed_source'),
    url(r'^api/feeds/updatefavorite/(?P<pk>.+)$', FavoriteUpdate.as_view(), name = 'feed_source'),
    url(r'^api/feeds/exclude/$', ExcludeViewSet.as_view(), name = 'feed_exclude'),
	url(r'^api/feeds/destroy/(?P<source>.+)$', ExcludeDestroyViewSet.as_view(), name = 'destroy'),



]
