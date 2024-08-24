from django.db import models

# Create your models here.
class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')
    document_name = models.CharField(max_length=255)  # Field for document name
    document_type = models.CharField(max_length=100)  # Field for document type
    extracted_text = models.TextField(blank=True, null=True)  # Field for storing extracted text
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.document_name + ' - ' + self.document_type
    
class DocumentVerification(models.Model):
    document_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    cert_number = models.CharField(max_length=50)
    date_of_completion = models.DateField()

    def __str__(self):
        return self.document_name  
