from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignerViewSet


router = DefaultRouter()
router.register(r'signers', SignerViewSet, basename='signer')

urlpatterns = [
    path('', include(router.urls)),
]


