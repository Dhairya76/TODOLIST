from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TODO(models.Model):
    status_choices = [
        ('C', 'Completed'),
        ('P', 'Pending'),
    ]
    priority_choices = [
        ('1', 'Very Important'),
        ('2', 'Important'),
        ('3', 'Least Important'),
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices=status_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2, choices=priority_choices)
    category = models.CharField(max_length=50 , default="Work")

class SubTask(models.Model):
    status_choices = [
        ('C', 'Completed'),
        ('P', 'Pending'),
    ]
    priority_choices = [
        ('1', 'Very Important'),
        ('2', 'Important'),
        ('3', 'Least Important'),
    ]
    subtask_title = models.CharField(max_length=50)
    subtask_status = models.CharField(max_length=2, choices=status_choices)
    subtask_priority = models.CharField(max_length=2, choices=priority_choices)
    todo = models.ForeignKey(TODO, on_delete=models.CASCADE , null=True)

