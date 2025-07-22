from rest_framework import serializers
from .models import Task, SubTask, Category
from rest_framework.exceptions import ValidationError
from datetime import datetime

class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =['title','description', 'status', 'deadline']
        

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'task', 'status', 'deadline', 'created_at']
        


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')

        if Category.objects.filter(name=name).exists():
            raise ValidationError ("Category with this name already exists")
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)

        if name != instance.name and Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise ValidationError({"name": "Category with this name already exists."})

        return super().update(instance, validated_data)


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields =['title','description', 'status', 'deadline', 'subtasks']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =['title','description', 'status', 'deadline']

    def validate_deadline(self, value):
        if value is None:
            return value
        today = datetime.now()
        
        if value < today:
            raise serializers.ValidationError("Deadline date cannot be in past")
        return value