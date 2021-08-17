from django.contrib import admin
from django.urls import path, include

from Task import settings


urlpatterns = [
    path('', include('Task.Program.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
