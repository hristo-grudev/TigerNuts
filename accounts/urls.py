from django.urls import path

from accounts.views import register, adduser

urlpatterns = [
	path('', register, name='register'),
	path('adduser/', adduser, name='adduser'),

]