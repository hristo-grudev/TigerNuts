from django import forms

from blog.models import Article


class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'description', 'slug', 'image', )

	def __init__(self, *args, **kwargs):
		super(ArticleForm, self).__init__(*args, **kwargs)

		self.fields['title'].widget.attrs['class'] = 'form-control'
		self.fields['description'].widget.attrs['class'] = 'form-control'
		self.fields['slug'].widget.attrs['class'] = 'form-control'
		self.fields['image'].widget.attrs['class'] = 'form-control'