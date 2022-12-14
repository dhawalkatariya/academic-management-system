from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
# Create your models here.


class Class(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_classes")
    name = models.CharField(max_length=40)
    invitation_code = models.CharField(
        max_length=15, blank=True)
    students = models.ManyToManyField(User, related_name="joined_classes")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.created_by.username})"

    def save(self, *args, **kwargs):
        self.invitation_code = get_random_string()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Classes"

# class Material(models.Model):
#     classroom = models.ForeignKey(
#         Class, related_name="material", on_delete=models.CASCADE)
#     message = models.TextField()
#     url = models.URLField(blank=True, null=True)
#     attachment = models.FileField(upload_to='attachment/', blank=True)
#     arrived = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Added to class {classroom} on {arrived}"
