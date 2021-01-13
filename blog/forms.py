from django import forms

from blog.models import Article, ArticleComments


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


class CommentForm(forms.ModelForm):
	class Meta:
		model = ArticleComments
		fields = ('message', )

	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)

		self.fields['message'].widget.attrs['class'] = 'form-control'
