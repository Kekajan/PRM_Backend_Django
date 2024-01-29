from rest_framework import serializers
from prm.models import Project, Task
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_superuser', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
