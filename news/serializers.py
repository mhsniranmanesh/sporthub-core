from rest_framework import serializers

from news.models import News


class NewsGetRecentSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('uuid', 'title', 'body' ,'tags', 'date_created')