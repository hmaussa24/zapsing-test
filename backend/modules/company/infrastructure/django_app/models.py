from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    api_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company'


