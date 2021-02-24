import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, ArticleComments
from common.models import OrderItem


def get_user(request):
    try:
        device = request.COOKIES['device']
    except:
        device = ''
    if request.user.is_authenticated:
        user = request.user
    else:
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
		context['user'] = user
		return context


class SingleArticleView(DetailView):
	permission_required = 'accounts.action_all'
	template_name = 'blog-single.html'
	context_object_name = 'article'
	model = Article

	def get_context_data(self, **kwargs):
		context = super(SingleArticleView, self).get_context_data()
		object_list = Article.objects.order_by('-date')[:3]
		form = CommentForm()
		user = get_user(self.request)
		comments = ArticleComments.objects.filter(article_title__exact=context['object'])
		comments_count = ArticleComments.objects.filter(article_title__exact=context['object']).count()

		if user:
			user_group = user.groups.filter(name='Admin').exists()
		else:
			user_group = False

		context['user_group'] = user_group
		context['comments_count'] = comments_count
		context['user'] = user
		context['object_list'] = object_list
		context['comments'] = comments
		context['form'] = form

		return context


class NewArticle(LoginRequiredMixin, FormView):
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
		context['user'] = user

		return context


class UpdateArticle(LoginRequiredMixin, UpdateView):
	model = Article
	template_name = 'update_article.html'
	form_class = ArticleForm

	def get_context_data(self, **kwargs):
		context = super(UpdateArticle, self).get_context_data()
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		context['user'] = user
		if user:
			user_group = user.groups.filter(name='Admin').exists()
		else:
			user_group = False

		context['user_group'] = user_group

		return context


class DeleteArticle(LoginRequiredMixin, DeleteView):
	model = Article
	template_name = 'delete_article.html'
	success_url = reverse_lazy('view blog')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		context['user'] = user
		if user:
			user_group = user.groups.filter(name='Admin').exists()
		else:
			user_group = False

		context['user_group'] = user_group
		return context


class CreateArticle(LoginRequiredMixin, CreateView):
	model = Article
	fields = ('title', 'description', 'slug', 'image', )

	def form_valid(self, form):
		form.instance.author_id = self.request.user.id
		text = form.instance.description
		form.instance.description = '<p>' + re.sub('\n', '</p>\n<p>', text) + '</p>'
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		context['user'] = user
		return context


class LeaveComment(LoginRequiredMixin, CreateView):
	model = ArticleComments
	form_class = CommentForm

	def form_valid(self, form):
		form.instance.author_id = self.request.user.id
		article = Article.objects.filter(slug=self.kwargs['slug'])
		form.instance.article_title_id = article[0].id

		return super().form_valid(form)

	def get_success_url(self):
		slug = self.kwargs['slug']
		return reverse_lazy('view article', kwargs={'slug': str(slug)})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		context['user'] = user
		return context


class DeleteComment(LoginRequiredMixin, DeleteView):
	model = ArticleComments
	template_name = 'delete_comment.html'
	success_url = reverse_lazy('view blog')

	def get_success_url(self):
		slug = self.kwargs['slug']
		return reverse_lazy('view article', kwargs={'slug': str(slug)})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		context['user'] = user
		context['slug'] = self.kwargs['slug']
		if user:
			user_group = user.groups.filter(name='Admin').exists()
		else:
			user_group = False

		context['user_group'] = user_group
		return context


class EditComment(LoginRequiredMixin, UpdateView):
	model = ArticleComments
	template_name = 'edit_comment.html'
	form_class = CommentForm

	def get_success_url(self):
		slug = self.kwargs['slug']
		return reverse_lazy('view article', kwargs={'slug': str(slug)})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list
		user = get_user(self.request)
		context['user'] = user
		context['slug'] = self.kwargs['slug']
		if user:
			user_group = user.groups.filter(name='Admin').exists()
		else:
			user_group = False

		context['user_group'] = user_group
		return context
