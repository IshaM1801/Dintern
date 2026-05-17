import uuid
from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    experience = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
