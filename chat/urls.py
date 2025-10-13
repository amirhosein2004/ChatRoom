from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings

urlpatterns = [
    # app admin
    path('admin/', admin.site.urls),
    # app room
    path('api/room/', include('app_room.urls')),
]

if (
    settings.DEBUG
    and getattr(settings, "ENVIRONMENT", "development") in {"development", "staging"}
):
    # debug toolbar
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
