from django.db import models
from django.contrib.auth.models import User
from classroom.models import Class

# Create your models here.


class Discussion(models.Model):
    created_by = models.ForeignKey(
        User, related_name="discussions", on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Class, related_name="discussions", on_delete=models.CASCADE)
    question = models.TextField(blank=False, null=False)
    submitted_on = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return f"Q{self.id} : {self.question}"

    class Meta:
        ordering = ('-submitted_on',)


class Response(models.Model):
    discussion = models.ForeignKey(
        Discussion, related_name="answers", on_delete=models.CASCADE)
    by = models.ForeignKey(User, related_name="answers",
                           on_delete=models.CASCADE)
    answer = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ans {self.id} - {self.answer}"

    class Meta:
        ordering = ("-submitted_on",)
