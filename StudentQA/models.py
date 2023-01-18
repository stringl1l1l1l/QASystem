from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class QuestionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stu_user_id_fk')
    question_text = models.CharField(max_length=1000, null=False)
    answer_text = models.CharField(max_length=1000, blank=True, null=False)
    ask_time = models.DateTimeField(null=False, auto_now_add=True)
    similar_question = models.CharField(max_length=1000, blank=True, null=False)
    is_helpful = models.BooleanField(null=False, default=True)

    # def __str__(self):
    #     return self.user.username + ": " + self.question_text

    class Meta:
        ordering = ["-ask_time"]


class Student(models.Model):
    number = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=20, null=False)
    work = models.CharField(max_length=100, null=False, default="")
    attendance = models.CharField(max_length=100, null=False)


class Course(models.Model):
    title = models.CharField(max_length=100, null=False)
    time = models.CharField(max_length=100, null=False, default="")
    content = models.CharField(max_length=200, null=False)
    teacher = models.CharField(max_length=20, null=False)
