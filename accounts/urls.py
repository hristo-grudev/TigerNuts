from django.urls import path

from accounts.views import register, login_user, logout_user, register_user

urlpatterns = [
	path('adduser/', register_user, name='adduser'),
	path('login/', login_user, name='view login'),
	path('logout/', logout_user, name='view logout'),
	path('register/', register, name='view register'),

]