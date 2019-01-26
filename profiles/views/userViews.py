from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from profiles.serializers import (
    CreateUserSerializer,
    UserUpdateInfosSerializer,
    UserGetPublicInfosSerializer, UserGetInitialInfosSerializer)
from profiles.models import User
from rest_framework import status

from profiles.utils.profilePictureUtils import generate_resized_profile_picture, generate_avatar

class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    lookup_field = 'email'


class UserUpdateInfosView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = UserUpdateInfosSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                if 'title' in serializer.validated_data.keys():
                    user.title = serializer.validated_data['title']
                if 'bio' in serializer.validated_data.keys():
                    user.bio = serializer.validated_data['bio']
                if 'profile_picture' in serializer.validated_data.keys():
                    user.profile_picture = serializer.validated_data['profile_picture']
                    user.avatar = serializer.validated_data['profile_picture']
                user.save()
                generate_resized_profile_picture(user.profile_picture)
                generate_avatar(user.avatar)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except:
                return Response(data={'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetPublicInfosView(RetrieveAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserGetPublicInfosSerializer
    lookup_field = 'username'


class UserExistsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        try:
            User.objects.get(username=username)  # retrieve the user using username
        except User.DoesNotExist:
            return Response(data={'username': 'OK'}, status=status.HTTP_200_OK)  # return false as user does not exist
        else:
            return Response(data={'username': 'A user with that username already exists.'}, status=status.HTTP_200_OK)  # Otherwise, return True


class UserGetInitialInfosView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            username = request.user.username
            try:
                user = User.objects.get(username=username)  # retrieve the user using username
                data = UserGetInitialInfosSerializer(user).data
                return Response(data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'username': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data={'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

