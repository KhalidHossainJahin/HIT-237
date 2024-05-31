from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),  # Ensure this line is included
    path('admins/', include('admins.urls')),
    path('studentGroup/', include('studentGroup.urls')),
    path('customUser/', include('customUser.urls')),
    path('notifications/', include('siteManagement.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
