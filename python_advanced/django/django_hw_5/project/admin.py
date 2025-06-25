from django.contrib import admin
from project.models import Tag, Project, Developer, Task
# Register your models here.

# admin.site.register(Tag)
# admin.site.register(Project)
# admin.site.register(Developer)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProjectAdmin(admin.ModelAdmin):
    # list_display = ('name', 'description', 'lang', 'created_at')
    # search_fields = ('name', 'description', 'lang', 'created_at')
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description', 'lang', 'created_at')
    readonly_fields = ('created_at',)

class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade')
    search_fields = ('name', 'grade')


class TaskAdmin(admin.ModelAdmin):
    # list_display = ('name', 'description', 'status', 'priority', 'created_at', 'updated_at')
    # search_fields = ('name', 'description', 'status', 'priority', 'created_at', 'updated_at')
    list_display = ('name', 'project__name', 'status', 'priority', 'created_at', 'due_date')
    # search_fields = ('name', 'description', 'status', 'priority', 'created_at', 'updated_at')
    # list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('status', 'priority', 'project__name', 'created_at', 'due_date')

admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Task, TaskAdmin)


#superuser login - admin superuser pass - qwerty2008