from django.contrib import admin

# Register your models here.
from news.models import News, NewsTag

admin.site.register(News)
admin.site.register(NewsTag)