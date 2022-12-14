from django.db import models
from classroom.models import Class


# Create your models here.


class Material(models.Model):
    classroom = models.ForeignKey(
        Class, related_name="material", on_delete=models.CASCADE)
    message = models.TextField()
    url = models.URLField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachment/', blank=True, null=True)
    arrived = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Added to class {self.classroom} on {self.arrived}"

    class Meta:
        ordering = ('-arrived',)
