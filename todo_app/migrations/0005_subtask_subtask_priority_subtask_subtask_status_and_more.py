# Generated by Django 4.2.3 on 2023-07-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0004_todo_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='subtask_priority',
            field=models.CharField(choices=[('1', 'Very Important'), ('2', 'Important'), ('3', 'Least Important')], default=2, max_length=2),
        ),
        migrations.AddField(
            model_name='subtask',
            name='subtask_status',
            field=models.CharField(choices=[('C', 'Completed'), ('P', 'Pending')], default='P', max_length=2),
        ),
        migrations.AddField(
            model_name='subtask',
            name='subtask_title',
            field=models.CharField(default='Subtask', max_length=50),
        ),
    ]
