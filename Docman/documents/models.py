from django.db import models
from django.contrib.auth.models import User

class DocumentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to='documents/', blank=True, null=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class DocumentFile(models.Model):
    document = models.ForeignKey(Document, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.document.title} - {self.file.name}"