from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class QuestionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='law_user_id_fk')
    question_text = models.CharField(max_length=1000, null=False)
    answer_text = models.CharField(max_length=1000, blank=True, null=False)
    ask_time = models.DateTimeField(null=False, auto_now_add=True)
    is_helpful = models.BooleanField(null=False, default=True)

    # def __str__(self):
    #     return self.user.username + ": " + self.question_text

    class Meta:
        ordering = ["-ask_time"]