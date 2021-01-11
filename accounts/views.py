from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import RegistrationData
from django.contrib import messages

def register(request):
	context = {
		'form': RegistrationForm
	}
	return render(request, 'register.html', context)


def adduser(request):
	form = RegistrationForm(request.POST)

	if form.is_valid():
		myregister = RegistrationData(username=form.cleaned_data['username'],
		                              password=form.cleaned_data['password'],
		                              email=form.cleaned_data['email'],
		                              phone=form.cleaned_data['phone'])
		myregister.save()
		messages.add_message(request, messages.SUCCESS, "You have registered successfully")
	return redirect('register')
