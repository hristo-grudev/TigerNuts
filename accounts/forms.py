from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
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
		widgets = {
			'date_of_birth': forms.DateInput(format=('%Y-%m-%d'),
											 attrs={'class': 'form-control', 'placeholder': 'Select a date',
													'type': 'date'}),
		}

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['date_of_birth'].required = False
		self.fields['profile_image'].required = False
		self.fields['profile_image'].widget.attrs['class'] = 'img-thumbnail'


class ProfileUpdateForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', )

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].label = "Потребителско име:"
		self.fields['username'].help_text = None
		self.fields['password'].label = 'Парола:'
		# self.fields['password'].help_text = None
		self.fields['first_name'].widget.attrs['class'] = 'form-control'
		self.fields['first_name'].label = "Име:"
		self.fields['last_name'].widget.attrs['class'] = 'form-control'
		self.fields['last_name'].label = "Фамилия:"
		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['email'].label = "E-mail:"

	def clean_email(self):
		email = self.cleaned_data.get('email', False)  # if have email return it else return False
		if not email:
			raise forms.ValidationError('Email is required')
		return email


class PassChangeForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

	class Meta:
		model = User
		fields = ('old_password', 'new_password1', 'new_password2', )

	def __init__(self, *args, **kwargs):
		super(PassChangeForm, self).__init__(*args, **kwargs)
		self.fields['old_password'].label = "Стара парола"
		self.fields['new_password1'].label = "Нова парола"
		self.fields['new_password2'].label = "Потвърди нова парола"
