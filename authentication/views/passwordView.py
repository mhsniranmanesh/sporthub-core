from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from authentication.utils import create_token
from profiles.models import User
from authentication.serializers.passwordSerializer import PasswordResetSerializer, ForgotPasswordSerializer
from authentication.models.passwordReset import PasswordReset


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(data={'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                uid = urlsafe_base64_encode(force_bytes(user.uuid))
                token = default_token_generator.make_token(user)
            except:
                return Response(data={'message': 'Failed to generate password reset'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not PasswordReset.objects.filter(user=user, is_used=False).exists():
                try:
                    password_reset = PasswordReset(user=user, token=token)
                    password_reset.save()
                except:
                    return Response(data={'message': 'Failed to save password reset'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                user.send_passwordreset_email(uid, token)
            except:
                return Response(data={'message': 'Failed to send password reset email'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data={'message': 'Password reset successfully sent'},
                                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response(data={'message': 'Password successfully changed'})
            except:
                return Response(data={'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckResetPasswordTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        if uidb64 is not None and token is not None:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(uuid=uid)
                password_reset = PasswordReset.objects.get(user=user, is_used=False)
                password_reset.is_used = True
                password_reset.save()
                if default_token_generator.check_token(user, token):
                    login_token = create_token(user)
                    return Response(data={'token': login_token})
                return Response(data={'message': 'Token Is Not Valid'}, status=status.HTTP_400_BAD_REQUEST)
            except PasswordReset.DoesNotExist:
                return Response(data={'message': 'Token Is Not Valid'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response(data={'message': 'Token Is Not Valid'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'message': 'Password reset token has not been provided'},
                        status=status.HTTP_400_BAD_REQUEST)

