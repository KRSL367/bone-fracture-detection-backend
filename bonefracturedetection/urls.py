
from django.contrib import admin 
from django.urls import path, include
from core.views import UserViewSet 

admin.site.site_header = 'Bfd Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('laboratory/', include('laboratory.urls')),
    path('auth/users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("__debug__/", include("debug_toolbar.urls")),
]