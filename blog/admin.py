from django.contrib import admin

from blog.models import Article, ArticleComments

admin.site.register(Article)
admin.site.register(ArticleComments)

