from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, ArticleComments
from common.models import OrderItem


def get_user(request):
	if request.user.is_authenticated:
		user = request.user
	else:
		try:
			device = request.COOKIES['device']
		except:
			device = ''
		user = User.objects.filter(username__exact=device).first()
	return user

class ArticleView(ListView):
	permission_required = 'accounts.action_all'
	template_name = 'blog.html'
	context_object_name = 'blog'
	model = Article

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = get_user(self.request)
		cart_items = OrderItem.objects.filter(user=user).filter(ordered=False).count()
		context['cart_items'] = cart_items
		return context


class SingleArticleView(DetailView):
	permission_required = 'accounts.action_all'
	template_name = 'blog-single.html'
	context_object_name = 'article'
	model = Article

	def get_context_data(self, **kwargs):
		context = super(SingleArticleView, self).get_context_data()
		object_list = Article.objects.order_by('date')[:3]
		form = CommentForm()
		user = get_user(self.request)
		comments = ArticleComments.objects.filter(article_title__exact=context['object'])
		cart_items = OrderItem.objects.filter(user=user).filter(ordered=False).count()
		context['cart_items'] = cart_items
		context['object_list'] = object_list
		context['comments'] = comments
		context['form'] = form

		return context


class NewArticle(FormView):
	template_name = 'new_article.html'
	form_class = ArticleForm
	success_url = 'view blog'

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.send_email()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(NewArticle, self).get_context_data()
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		cart_items = OrderItem.objects.filter(user=user).filter(ordered=False).count()
		context['cart_items'] = cart_items

		return context


class CreateArticle(CreateView):
	model = Article
	fields = ('title', 'description', 'slug', 'image', )

	def form_valid(self, form):
		form.instance.author_id = self.request.user.id
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = get_user(self.request)
		cart_items = OrderItem.objects.filter(user=user).filter(ordered=False).count()
		context['cart_items'] = cart_items
		return context


class LeaveComment(CreateView):
	model = ArticleComments
	fields = ('message',)
	success_url = reverse_lazy("view blog")

	def form_valid(self, form):
		# comment = form.save(commit=False)
		# comment.author = self.request.user
		form.instance.author_id = self.request.user.id
		form.instance.article_title_id = 2
		# comment.article_title = 2
		# comment.save()
		print(2)
