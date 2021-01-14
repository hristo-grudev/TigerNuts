from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	slug = models.SlugField()
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='media')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_of_article', default=1)

	def __str__(self):
		return self.title

	def snippet(self):
		return self.description[:200]

	def get_absolute_url(self):
		return reverse('view article', kwargs={'slug': self.slug})

	class Meta:
		ordering = ('-date', )


class ArticleComments(models.Model):
	article_title = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_title', default=None)
	date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', default=None)
	message = models.TextField(max_length=500, default=None)

	def __str__(self):
		return f'{self.author} - {self.article_title}'

	class Meta:
		ordering = ('date', )
