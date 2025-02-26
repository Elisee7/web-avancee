# accounts/serializers.py

from rest_framework import serializers
from .models import User, Student, ParentChild

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'date_joined']
        read_only_fields = ['date_joined']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name', 'role']
    
    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'class_level', 'birth_date', 'school']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    
    class Meta:
        model = Student
        fields = ['user', 'class_level', 'birth_date', 'school']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'student'
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        student = Student.objects.create(user=user, **validated_data)
        return student

class ParentChildSerializer(serializers.ModelSerializer):
    parent_details = UserSerializer(source='parent', read_only=True)
    child_details = UserSerializer(source='child', read_only=True)
    
    class Meta:
        model = ParentChild
        fields = ['id', 'parent', 'child', 'parent_details', 'child_details']
        read_only_fields = ['id']