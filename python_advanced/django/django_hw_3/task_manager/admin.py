from django.contrib import admin

# Register your models here.
from task_manager.models import Task, SubTask, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline', 'created_at')
    list_filter = ('title', 'description', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('title',)
    fields = ('title', 'description', 'status', 'deadline')
    list_per_page = 5

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description', 'task')
    ordering = ('title',)
    fields = ('title', 'description', 'task', 'status', 'deadline')
    list_per_page = 5

admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)