import uuid
from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    condition = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
