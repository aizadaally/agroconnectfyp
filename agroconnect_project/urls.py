# agroconnect_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# Non-translated URL patterns
urlpatterns = [
    # This is critical for language switching to work
    path('i18n/', include('django.conf.urls.i18n')),
    # Place API paths outside of i18n patterns
    path('api/', include('api.urls')),
]

# Translated URL patterns
urlpatterns += i18n_patterns(
    path(_('admin/'), admin.site.urls),
    # Don't include API here - it should be in the non-translated section
    path('', include('frontend.urls')),
    prefix_default_language=True  # Keep language prefix for consistency
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # new
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # new