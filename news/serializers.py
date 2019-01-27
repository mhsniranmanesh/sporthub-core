from rest_framework import serializers

from news.models import News, NewsTag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ['name']

class NewsGetRecentSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = News
        fields = ('uuid', 'title', 'body', 'tag','date_created')