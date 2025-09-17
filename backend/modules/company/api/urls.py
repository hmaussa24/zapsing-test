from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet
from .auth_views import register, login, me


router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register', register),
    path('auth/login', login),
    path('auth/me', me),
]


