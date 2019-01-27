from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from news.views import NewsGetRecent, NewsGetRecentFollowing

urlpatterns = {
    url(r'^recent/$', NewsGetRecent.as_view(), name="get-recent-news"),
    url(r'^recent/following/$', NewsGetRecentFollowing.as_view(), name="get-recent-following-news"),
    }

urlpatterns = format_suffix_patterns(urlpatterns)
