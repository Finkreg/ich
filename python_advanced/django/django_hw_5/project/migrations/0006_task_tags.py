# Generated by Django 5.2.1 on 2025-06-23 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_task_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='project.tag'),
        ),
    ]
