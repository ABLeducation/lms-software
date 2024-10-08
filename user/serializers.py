from rest_framework import serializers # type: ignore
from .models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token # type: ignore

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
        fields = ("__all__")

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

class SchoolSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = School
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        school = School.objects.create(user=user, **validated_data)
        return school

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        if username_or_email and password:
            # Check if the input is an email
            if '@' in username_or_email:
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                    username = user_obj.username
                except CustomUser.DoesNotExist:
                    raise serializers.ValidationError("User with this email does not exist")
            else:
                username = username_or_email
            
            # Authenticate with username
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include 'username_or_email' and 'password'")

        data['user'] = user
        return data
    
class UserLoginActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginActivity
        fields = '__all__'
        
class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity1
        fields = '__all__'
        
class MacroplannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Macroplanner
        fields = '__all__'
        
class MicroplannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microplanner
        fields = '__all__'
        
class AdvocacyVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvocacyVisit
        fields = '__all__' 
        
class NotificationStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationStudent
        fields = '__all__'