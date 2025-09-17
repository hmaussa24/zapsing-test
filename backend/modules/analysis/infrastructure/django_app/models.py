from django.db import models


class DocumentAnalysis(models.Model):
    document = models.OneToOneField('documents.Document', on_delete=models.CASCADE, related_name='analysis', db_index=True)
    summary = models.TextField(blank=True, default='')
    labels = models.JSONField(default=list)
    entities = models.JSONField(default=list)
    risk_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'document_analysis'

