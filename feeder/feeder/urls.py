from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken import views
from feeds.views import FeedViews, FeedSource, ExcludeViewSet, FavoriteViews, FavoriteUpdate, ExcludeDestroyViewSet, UserViews, UserUpdate

router = routers.SimpleRouter()
# router.register (r'destroy', ExcludeDestroyViewSet)

urlpatterns = [

    # Examples:
    # url(r'^$', 'feeder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ap/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls',
                               # namespace='rest_framework')),
    # url(r'^auth/', views.obtain_auth_token),
    url(r'^rest-auth/', include('rest_auth.urls')),

    # url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    # url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),
    url(r'^api/feeds/$', FeedViews.as_view(), name = 'feeds'),
    url(r'^api/feeds/source/$', FeedSource.as_view(), name = 'feed_source'),
    url(r'^api/feeds/favorite/$', FavoriteViews.as_view(), name = 'feed_source'),
    url(r'^api/feeds/updatefavorite/(?P<pk>.+)$', FavoriteUpdate.as_view(), name = 'feed_source'),
    url(r'^api/feeds/exclude/$', ExcludeViewSet.as_view(), name = 'feed_exclude'),
	url(r'^api/feeds/destroy/(?P<source>.+)$', ExcludeDestroyViewSet.as_view(), name = 'destroy'),
    url(r'^api/feeds/users/$', UserViews.as_view(), name = 'user'),
    url(r'^api/feeds/userupdate/(?P<pk>[0-9]+)$', UserUpdate.as_view(), name = 'userupdate'),

]
