from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, ObtainJSONWebToken
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from authentication.serializers.loginSerializer import LoginWithUsernameOrPasswordJWTSerializer
from .views import EmailActivationView, ForgotPasswordView, ResetPasswordView, CheckResetPasswordTokenView


urlpatterns = {
    url(r'^token/obtain/$', obtain_jwt_token, name='get-jwt-token'),
    url(r'^login/$', ObtainJSONWebToken.as_view(serializer_class=LoginWithUsernameOrPasswordJWTSerializer),
        name='get-jwt-token'),
    url(r'^token/refresh/$', refresh_jwt_token, name='refresh-jwt-token'),
    url(r'^token/verify/$', verify_jwt_token, name='verify-jwt-token'),
    url(r'^verify-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', EmailActivationView.as_view(),
        name='email-activation-link'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(),
        name='forgot-password'),
    url(r'^reset-password/$', ResetPasswordView.as_view(),
        name='forgot-password'),
    url(r'^check-password-token/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', CheckResetPasswordTokenView.as_view(),
        name='reset-password'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
