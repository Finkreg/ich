from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

TAG_CHOICES = {
    'db_backend': 'Backend',
    'db_frontend': 'Frontend',
    'db_q&a': 'Q&A',
    'db_design': 'Design',
    'db_devops': 'DevOps',
}
class Tag(models.Model):
    name = models.CharField(max_length=50, choices=TAG_CHOICES, unique=True)
    projects = models.ManyToManyField('Project', related_name='tags', null=True, blank=True)
    # description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

LANG_CHOICES = {
    'py': 'Python',
    'js': 'JavaScript',
    'c#': 'C#',
}

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField(choices=LANG_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
GRADE_CHOICES = {
    'sn': 'Senior',
    'md': 'Middle',
    'jn': 'Junior',
    'tl': 'TeamLead',
}
class Developer(models.Model):
    name = models.CharField(max_length=50)
    grade = models.CharField(choices=GRADE_CHOICES)
    projects = models.ManyToManyField('Project', related_name='devs', null=True, blank=True)

STATUS_CHOICES = {
    'new': 'New',
    'in_progress': 'In Progress',
    'done': 'Done',
    'closed': 'Closed',
    'blocked': 'Blocked',
    'pending': 'Pending',
}

PRIORITY_CHOICES = {
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High',
    'very_high': 'Very High',
}
class Task(models.Model):
    name = models.CharField(validators=[MinLengthValidator(10)], unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)