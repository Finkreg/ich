from rest_framework import serializers
from .models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    """For objects serializing """

    class Meta:
        model = Project
        fields = ['id', 'name', 'description']