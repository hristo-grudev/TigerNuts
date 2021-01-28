from django.contrib.auth.decorators import login_required
from django.urls import path

from blog.views import ArticleView, SingleArticleView, CreateArticle, NewArticle, LeaveComment, UpdateArticle, \
	DeleteArticle, DeleteComment, EditComment

urlpatterns = [
	path('', ArticleView.as_view(), name='view blog'),
	path('article/<slug:slug>', SingleArticleView.as_view(), name='view article'),
	path('new', login_required(NewArticle.as_view(), login_url="view login"), name='new article'),
	path('article/edit/<slug:slug>', login_required(UpdateArticle.as_view(), login_url="view login"), name='edit article'),
	path('article/delete/<slug:slug>', login_required(DeleteArticle.as_view(), login_url="view login"), name='delete article'),
	path('create', login_required(CreateArticle.as_view(), login_url="view login"), name='create article'),
	path('article/<slug:slug>/comment', login_required(LeaveComment.as_view(), login_url="view login"), name='leave comment'),
	path('article/<slug:slug>/comment/edit/<int:pk>', login_required(EditComment.as_view(), login_url="view login"), name='edit comment'),
	path('article/<slug:slug>/comment/<int:pk>', login_required(DeleteComment.as_view(), login_url="view login"), name='delete comment'),

]
