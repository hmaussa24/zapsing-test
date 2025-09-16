from django.db import models


class Document(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.PROTECT, related_name='documents', db_index=True)
    name = models.CharField(max_length=255)
    pdf_url = models.URLField()
    status = models.CharField(max_length=50, default='created')
    open_id = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'document'


