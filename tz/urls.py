from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include("auth_sys.urls")),
    path('admin/', admin.site.urls),
    path('', include("bookmarks_service.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
