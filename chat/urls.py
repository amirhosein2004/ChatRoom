from django.contrib import admin
from django.urls import path

urlpatterns = [
    # app admin
    path('admin/', admin.site.urls),
]
