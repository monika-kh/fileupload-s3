from django.db import models

class EncryptedFile(models.Model):
    name = models.CharField(max_length=255)
    encrypted_data = models.BinaryField()
    upload_date = models.DateTimeField(auto_now_add=True)
