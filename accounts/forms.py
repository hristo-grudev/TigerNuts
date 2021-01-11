from django import forms


class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=100,
	                           widget=forms.TextInput(attrs={
		                           'class': 'form-control',
		                           'placeholder': 'Username'
	                           }))
	password = forms.CharField(max_length=100,
	                           widget=forms.PasswordInput(attrs={
		                           'class': 'form-control',
		                           'placeholder': 'Password'
	                           }))
	email = forms.EmailField(max_length=100,
	                         widget=forms.EmailInput(attrs={
		                         'class': 'form-control',
		                         'placeholder': 'Email'
	                         }))
	phone = forms.CharField(max_length=100,
	                        widget=forms.NumberInput(attrs={
		                        'class': 'form-control',
		                        'placeholder': 'Phone'
	                        }))
