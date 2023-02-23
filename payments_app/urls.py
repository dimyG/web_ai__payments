from django.urls import path
from .views import PaymentViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include

# app_name = 'payments_app'
router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
]
