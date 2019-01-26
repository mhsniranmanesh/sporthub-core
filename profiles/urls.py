from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from profiles.views import (
    UserCreateView,
    UserUpdateInfosView,
    UserExistsView,
    UserGetPublicInfosView,
)

urlpatterns = {
    url(r'^get-pub-infos/(?P<username>[-\w]+)/$', UserGetPublicInfosView.as_view(), name="get-profile-public-infos"),
    url(r'^$', UserCreateView.as_view(), name="create"),
    url(r'^userexists/(?P<username>[-\w]+)/$', UserExistsView.as_view(), name="exists"),
    url(r'^update-infos/$', UserUpdateInfosView.as_view(), name="update-profile-infos"),
    }

urlpatterns = format_suffix_patterns(urlpatterns)
