from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, FormView

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, ArticleComments


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
		object_list = Article.objects.order_by('date')[:3]
		form = CommentForm()
		comments = ArticleComments.objects.filter(article_title__exact=context['object'])
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

		return context


class CreateArticle(CreateView):
	model = Article
	fields = ('title', 'description', 'slug', 'image', )

	def get(self, request, *args, **kwargs):
		context = {'form': ArticleForm()}
		return render(request, 'blog.html', context)

	def post(self, request, *args, **kwargs):
		form = ArticleForm(request.POST, request.FILES)
		print(form.is_valid())
		if form.is_valid():
			article = form.save(commit=False)
			article.author = request.user
			print(article.image)
			article.save()
			return redirect('view blog')
		return redirect('view blog')


class LeaveComment(CreateView):
	model = ArticleComments
	fields = ('message', )

	def get_queryset(self):
		print(get_object_or_404(Article, slug=self.kwargs['article_slug']))
		return get_object_or_404(Article, slug=self.kwargs['article_slug'])

	def get_context_data(self, **kwargs):
		context = super(LeaveComment, self).get_context_data()
		print(context)

	def get(self, request, *args, **kwargs):
		context = {'form': ArticleForm()}
		return render(request, 'blog.html', context)

	def post(self, request, *args, **kwargs):
		form = ArticleForm(request.POST)
		print(request.POST['message'])
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.article_title = 2
			comment.save()
			return redirect('view blog')
		return redirect('view blog')

	def get_absolute_url(self):
		return reverse("view article", kwargs={"slug": self.slug})