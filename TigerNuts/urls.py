from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('auth/', include('accounts.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    path("robots.txt", robots_txt),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)