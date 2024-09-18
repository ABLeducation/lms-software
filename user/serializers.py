from rest_framework import serializers # type: ignore
from .models import Student, Teacher, School, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Student
        fields = ('user', 'name', 'grade', 'section', 'school')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ('user', 'school')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

class SchoolSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = School
        fields = ('user', 'school')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        school = School.objects.create(user=user, **validated_data)
        return school
