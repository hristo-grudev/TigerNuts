from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm, LoginForm, ProfileForm


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('view home')


def register(request):
    context = {
        'user_form': RegisterForm(),
        'profile_form': ProfileForm(),
    }
    return render(request, 'register.html', context)


@transaction.atomic  # изпълнява всички или нито една
def register_user(request):
    if request.method == 'GET':
        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }
        return render(request, 'register.html', context)
    else:
        device = request.COOKIES['device']
        user_exist = User.objects.filter(username__exact=device).first()
        if user_exist.username == device:
            user_form = RegisterForm(data=request.POST, instance=user_exist)
        else:
            user_form = RegisterForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        print(profile_form.errors)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # add user
            profile = profile_form.save(commit=False)  # не го запазва преди да направи връзката 1 към 1
            profile.user = user
            profile.save()

            login(request, user)  # login user
            return redirect('view home')

        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }
        return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'login.html', context)
    else:
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('view home')
        context = {
            'login_form': login_form
        }
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('view home')
