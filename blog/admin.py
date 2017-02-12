from django.contrib import admin
from .models import Post

class ArticleAdmin (admin.ModelAdmin):
    fields = ['title', 'text', 'published_date']

admin.site.register(Post, ArticleAdmin)
