from django.db import models


class Signer(models.Model):
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'signer'
        constraints = [
            models.UniqueConstraint(fields=['document', 'email'], name='uniq_document_email'),
        ]


