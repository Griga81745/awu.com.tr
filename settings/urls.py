from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('apps.users.urls')),
  path('api/', include('apps.api.urls')),
  path('we/', include('apps.we.urls')),
  path('blog/', include('apps.posts.urls')),
  path('messenger/', include('apps.messenger.urls')),
]

handler404 = "settings.views.page_404"

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )