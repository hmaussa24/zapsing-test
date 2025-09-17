from django.urls import path
from .views import analysis_webhook


urlpatterns = [
    path('webhooks/analysis/', analysis_webhook),
]

