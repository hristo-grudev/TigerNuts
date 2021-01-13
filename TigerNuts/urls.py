from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('auth/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)