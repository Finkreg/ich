# Generated by Django 5.2.1 on 2025-06-05 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_authordetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('timestamp', models.DateTimeField(verbose_name='Event date')),
                ('book', models.ManyToManyField(related_name='Event', to='library.book', verbose_name='Books')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.library', verbose_name='Library')),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateField(auto_now_add=True, verbose_name='register date')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.event')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.member')),
            ],
        ),
    ]
