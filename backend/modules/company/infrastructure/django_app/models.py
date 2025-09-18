from django.db import models
from django.db.models.functions import Lower


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    api_token = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company'
        constraints = [
            models.UniqueConstraint(Lower('email'), name='uniq_company_email_ci')
        ]
        indexes = [
            models.Index(Lower('email'), name='idx_company_email_ci')
        ]


