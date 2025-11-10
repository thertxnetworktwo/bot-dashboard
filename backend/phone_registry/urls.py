from django.urls import path
from .views import (
    PhoneCheckView,
    PhoneRegisterView,
    PhoneBulkRegisterView,
    PhoneCleanupView
)

urlpatterns = [
    path('phone/check', PhoneCheckView.as_view(), name='phone-check'),
    path('phone/register', PhoneRegisterView.as_view(), name='phone-register'),
    path('phone/bulk-register', PhoneBulkRegisterView.as_view(), name='phone-bulk-register'),
    path('phone/cleanup', PhoneCleanupView.as_view(), name='phone-cleanup'),
]
