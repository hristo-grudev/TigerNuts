from django.urls import path

from blog.views import ArticleView, SingleArticleView, CreateArticle, NewArticle

urlpatterns = [
	path('', ArticleView.as_view(), name='view blog'),
	path('article/<slug:slug>', SingleArticleView.as_view(), name='view article'),
	path('new', NewArticle.as_view(), name='new article'),
	path('create', CreateArticle.as_view(), name='create article'),

]
