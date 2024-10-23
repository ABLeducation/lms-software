from rest_framework import serializers # type: ignore
from .models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token # type: ignore

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'role')
        extra_kwargs = {'password': {'write_only': False}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    profile_pic = serializers.ImageField(max_length=None, use_url=False,required=False,allow_null=True)

    class Meta:
        model = Student
        fields = ['user','name','grade','section','school','profile_pic']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        user.is_active = False
        user.save()
        student = Student.objects.create(user=user, **validated_data)
        return student
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Use the request object to build the absolute URL
        request = self.context.get('request')
        if request:
            representation['profile_pic'] = request.build_absolute_uri(instance.profile_pic.url) if instance.profile_pic else None
        return representation

class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['user','name','school']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        user.is_active = False
        user.save()
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
    
class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['mobile_num', 'subject', 'designation','grades']


class SchoolSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    school = serializers.CharField(required=True)

    class Meta:
        model = School
        fields = ['user','school']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        user.is_active = False  # User is not active until verified
        user.save()

        # Create the school entry linked to the created user
        school = School.objects.create(user=user, **validated_data)
        return school
    
class SchoolProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'principal_name', 'principal_number', 'principal_email',
            'teacher_coordinator', 'teacher_coordinator_number', 'teacher_coordinator_email',
            'account_name', 'account_email', 'accountant_number',
            'city', 'state', 'country', 'geo_location'
        ]

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
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        # Check if a user with this email exists in the system
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email does not exist.")
        return value