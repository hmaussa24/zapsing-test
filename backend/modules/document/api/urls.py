from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet
from rest_framework.decorators import action


router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]


