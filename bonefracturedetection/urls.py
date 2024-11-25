
from django.contrib import admin 
from django.urls import path, include
from bonefracturedetection import settings
from core.views import CustomTokenCreateView, UserViewSet 
from django.conf.urls.static import static

admin.site.site_header = 'Bfd Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('laboratory/', include('laboratory.urls')),
    path('auth/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path("auth/jwt/create/", CustomTokenCreateView.as_view(), name="custom_register"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)