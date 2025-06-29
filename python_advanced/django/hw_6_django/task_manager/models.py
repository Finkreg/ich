from django.db import models
from django.db.models import UniqueConstraint
# Create your models here.

class Task(models.Model):
    status_choices = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('done', 'Done')
    ]
    title = models.CharField(max_length=100, verbose_name="Task title")
    description = models.CharField(max_length=200, verbose_name="Task description")
    category = models.ManyToManyField('Category', related_name="tasks", verbose_name='Categories')
    status = models.CharField(max_length=20, choices=status_choices,default='new', verbose_name='Task status')
    deadline = models.DateField(blank=True, null=True, verbose_name='Task deadline')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creation Date')

    def get_short_title(self):
        if len(self.title) > 5:
            return self.title[:5]+ "..."
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            UniqueConstraint(fields=['title'], name='unique_task_title')
        ]


    def __str__(self):
        return f'{self.title}: {self.description}'
    

class SubTask(models.Model):
    subtask_choices = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=100, verbose_name="Subtask title")
    description = models.CharField(max_length=200, verbose_name="Subtask description")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=subtask_choices,verbose_name='Subtask status')
    deadline = models.DateField(blank=True, null=True, verbose_name='Subtask deadline')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        constraints = [
            UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]


    def __str__(self):
        return f'{self.title}: {self.description}'

class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Category name')

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            UniqueConstraint(fields=['name'], name='unique_category_name')
        ]

    def __str__(self):
        return self.name