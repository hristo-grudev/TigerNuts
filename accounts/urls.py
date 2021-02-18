from django.contrib.auth import views
from django.urls import path

from accounts.views import login_user, logout_user, register_user, PasswordsChangeView, ProfileView, password_changed, \
	ShowProfilePageView

urlpatterns = [
	path('adduser/', register_user, name='adduser'),
	path('login/', login_user, name='view login'),
	path('logout/', logout_user, name='view logout'),
	path('register/', register_user, name='view register'),
	# path('register/', UserRegisterView.as_view(), name='view register')
	path('password/', PasswordsChangeView.as_view()),
	path('password_changed/', password_changed, name="password_changed"),
	path('profile_edit/', ProfileView.as_view(), name='edit profile'),
	path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='view profile'),

]