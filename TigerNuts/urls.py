from django.contrib import admin
from django.urls import path, include

from accounts.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('register/', include('accounts.urls'))
]
