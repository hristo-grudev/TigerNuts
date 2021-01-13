from django import forms
from django.views.generic import ListView, DetailView, CreateView, FormView

from blog.forms import ArticleForm
from blog.models import Article


class ArticleView(ListView):
	permission_required = 'accounts.action_all'
	template_name = 'blog.html'
	context_object_name = 'blog'
	model = Article


class SingleArticleView(DetailView):
	permission_required = 'accounts.action_all'
	template_name = 'blog-single.html'
	context_object_name = 'article'
	model = Article

	def get_context_data(self, **kwargs):
		context = super(SingleArticleView, self).get_context_data()
		object_list = Article.objects.order_by('-date')[:3]
		context['object_list'] = object_list

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


class CreateArticle(CreateView):
	model = Article
	fields = ('title', 'description', 'slug', 'image', )
