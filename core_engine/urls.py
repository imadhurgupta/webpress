"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),   # Google OAuth + allauth endpoints
    path('', include('core_app.urls')),
    # Serve favicon from root
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': settings.STATICFILES_DIRS[0]}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'core_app.views.platform.error_404'
handler500 = 'core_app.views.platform.error_500'
