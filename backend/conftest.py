import pytest
from django.conf import settings

@pytest.fixture(autouse=True, scope="session")
def django_settings():
    settings.DEBUG = False
    return settings
