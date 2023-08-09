from django.forms import ModelForm
from django import forms

from todo_app.models import TODO , SubTask


class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'category', 'status', 'priority']


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['subtask_title', 'subtask_status', 'subtask_priority'] 