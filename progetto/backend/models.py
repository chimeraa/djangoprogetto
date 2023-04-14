from django.db import models


class QA(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.question
