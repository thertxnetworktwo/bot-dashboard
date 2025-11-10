"""
URL configuration for dashboard project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({'status': 'healthy'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health', health_check, name='health'),
    path('api/', include('products.urls')),
    path('api/', include('phone_registry.urls')),
]
