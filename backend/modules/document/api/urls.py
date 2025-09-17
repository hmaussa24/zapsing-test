from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet
from rest_framework.decorators import action
from .webhooks import zapsign_webhook


router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/zapsign/', zapsign_webhook),
]


