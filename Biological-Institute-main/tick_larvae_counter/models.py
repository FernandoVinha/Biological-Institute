from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Photo(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    processed_image = models.ImageField(upload_to='processed_photos/', blank=True, null=True)
    count_field = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    manual_count = models.IntegerField(blank=True, null=True)  # Campo para contagem manual

    def __str__(self):
        return f"Photo {self.id} uploaded by {self.uploaded_by}"
