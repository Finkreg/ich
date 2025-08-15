from rest_framework import serializers
from .models import Task, SubTask, Category
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


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
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # 🔐 хэширование
        user.save()
        return user