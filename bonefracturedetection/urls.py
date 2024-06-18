
from django.contrib import admin 
from django.urls import path, include 

admin.site.site_header = 'Bfd Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('laboratory/', include('laboratory.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('core.urls')),
]