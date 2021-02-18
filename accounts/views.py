from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import RegisterForm, LoginForm, ProfileForm, ProfileUpdateForm, PassChangeForm
from .models import UserProfile


def get_user(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            device = request.COOKIES['device']
        except:
            device = ''
        user = User.objects.filter(username__exact=device).first()
    return user


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('view home')


def register(request):
    user = get_user(request)
    print(user)
    context = {
        'user_form': RegisterForm(),
        'profile_form': ProfileForm(),
        'user': user,
    }
    return render(request, 'register.html', context)


@transaction.atomic  # изпълнява всички или нито една
def register_user(request):
    user = get_user(request)
    if request.method == 'GET':

        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
            'user': user,
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
            'user': user,
        }
        return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'GET':
        login_form = LoginForm()
        user = get_user(request)
        context = {
            'login_form': login_form,
            'user': user,
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
        user = get_user(request)
        context = {
            'login_form': login_form,
            'user': user,
        }
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('view home')


class PasswordsChangeView(PasswordChangeView):
    form_class = PassChangeForm
    template_name = 'change-password.html'
    success_url = reverse_lazy('password_changed')


def password_changed(request):
    return render(request, 'password_changed.html', {})


class ProfileView(UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('view home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_data = UserProfile.objects.filter(user=self.request.user)[0]
        initial_dict = {
            'date_of_birth': profile_data.date_of_birth,
            'profile_image': profile_data.profile_image,
        }
        profile_form = ProfileForm(initial=initial_dict)
        context['profile_form'] = profile_form
        return context

    def get_object(self):
        return self.request.user


class ShowProfilePageView(DetailView):
    Model = UserProfile
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(UserProfile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context

    def get_object(self):
        return self.request.user