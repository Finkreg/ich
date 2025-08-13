from rest_framework import serializers
from .models import Task, SubTask, Category
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone

class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =['id', 'title','description', 'status', 'deadline']
        

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']
        


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
        fields =['id', 'title','description', 'status', 'deadline', 'subtasks']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =['id', 'title','description', 'status', 'deadline', 'category']

    category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    many=True
    )

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        task = Task.objects.create(**validated_data)
        task.category.set(categories)
        return task


    def validate_deadline(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Deadline date cannot be in the past.")
        return value