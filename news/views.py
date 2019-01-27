from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News
from news.serializers import NewsGetRecentSerializer


class NewsGetRecent(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            latest_news = News.objects.order_by('-date_created')[:10]  # retrieve the user using username
            if len(latest_news) == 0 :
                return Response(data={'data': 'There is no recent news'}, status=status.HTTP_200_OK)
            data = []
            for news in latest_news:
                data.append(NewsGetRecentSerializer(news).data)
            return Response(data={'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Otherwise, return True


class NewsGetRecentFollowing(APIView):
    permission_classes = (AllowAny,)
    def get(self):
        try:
            latest_news = News.objects.order_by('-date_created')[:10]  # retrieve the user using username
            if len(latest_news) == 0 :
                return Response(data={'data': 'There is no recent news'}, status=status.HTTP_200_OK)
            data = NewsGetRecentSerializer(latest_news).data
            return Response(data={'data': data}, status=status.HTTP_200_OK)
        except :
            return Response(data={'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Otherwise, return True
