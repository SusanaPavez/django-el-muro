from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('core.urls')),
    path('wall/', include('wall.urls')),
    path('admin/', admin.site.urls),
]
