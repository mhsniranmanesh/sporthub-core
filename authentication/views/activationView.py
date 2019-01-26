from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from authentication.utils import create_token
from profiles.models import User


class EmailActivationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        if uidb64 is not None and token is not None:
            uid = force_text(urlsafe_base64_decode(uidb64))
            try:
                user = User.objects.get(uuid=uid)
                if default_token_generator.check_token(user, token) and user.is_active == False:
                    user.is_active = True
                    user.is_email_verified = True
                    user.save()
                    token = create_token(user)
                    return Response(data={'username': user.username, 'token': token, 'first_name': user.first_name,
                                          'last_name': user.last_name})
                return Response(data={'message': 'Token Is Not Valid'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={'message': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message': 'Token Has Not Been Provided'}, status=status.HTTP_400_BAD_REQUEST)
