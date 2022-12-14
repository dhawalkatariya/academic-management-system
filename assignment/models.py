from django.db import models
from django.contrib.auth.models import User
from classroom.models import Class


# Create your models here.


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    classroom = models.ForeignKey(
        Class, related_name="assignments", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Question(models.Model):
    assignment = models.ForeignKey(
        Assignment, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    c1 = models.CharField(max_length=100)
    c2 = models.CharField(max_length=100)
    c3 = models.CharField(max_length=100)
    c4 = models.CharField(max_length=100)
    answer = models.SmallIntegerField()

    def __str__(self):
        return f"{self.id} - {self.text}"


class GradedAssignment(models.Model):
    assignment = models.ForeignKey(
        Assignment, related_name="grades", on_delete=models.CASCADE)
    total_marks = models.SmallIntegerField(null=False)
    marks = models.SmallIntegerField(null=False)
    user = models.ForeignKey(
        User, related_name="grades", on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['assignment', 'user'], name='unique_for_user')
        ]

    def __str__(self):
        return f"{self.id}- {self.marks}/{self.total_marks}"
