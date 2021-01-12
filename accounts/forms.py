from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile


class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'email', )
		help_texts = {
			'username': None,
			'password1': None,
			'password2': None,
			'email': None,
		}

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['class'] = 'form-control'

	def clean_email(self):
		email = self.cleaned_data.get('email', False)  # if have email return it else return False
		if not email:
			raise forms.ValidationError('Email is required')
		return email


class LoginForm(AuthenticationForm):
	class Meta:
		model = User

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password'].widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		exclude = ('user',)

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['date_of_birth'].required = False
		self.fields['profile_image'].required = False
		self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'
		self.fields['profile_image'].widget.attrs['class'] = 'form-control'


