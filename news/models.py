from django.db import models
import uuid as uuid_lib
# Create your models here.
from django.utils import timezone


class NewsTag(models.model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(_('tag name'), max_length=64, blank=False)
    news = models.ForeignKey(News, related_name='news_tags', on_delete=models.CASCADE, blank=False)


class News(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=256, blank=False)
    body = models.CharField(_('body'), max_length=2000, blank=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)
