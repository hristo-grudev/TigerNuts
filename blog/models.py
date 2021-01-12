from django.db import models


class Article(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	slug = models.SlugField()
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='media/')

	def __str__(self):
		return self.title

	def snippet(self):
		return self.description[:200]

	class Meta:
		ordering = ('date', )

