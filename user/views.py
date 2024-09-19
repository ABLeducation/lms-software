from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .serializers import *
from django.contrib.auth import login
from django.utils import timezone

class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Print the entire data received
        user_data = request.data
        
        # Check if 'user' is a dictionary
        if not isinstance(user_data, dict):
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info = user_data.get('user', {})
        if not isinstance(user_info, dict):
            return Response({'error': 'Invalid user data format'}, status=status.HTTP_400_BAD_REQUEST)
        
        role = user_info.get('role')
        print("Role:", role)
        
        if role == 'student':
            serializer = StudentSerializer(data=user_data)
            
        elif role == 'teacher':
            serializer = TeacherSerializer(data=user_data)
            
        elif role == 'school':
            serializer = SchoolSerializer(data=user_data)
            
        else:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)  # Print errors if serializer is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginActivityView(APIView):
    def post(self, request):
        # Retrieve data from request
        login_ip = request.META.get('REMOTE_ADDR')
        user_agent_info = request.META.get('HTTP_USER_AGENT', 'unknown')  # Fallback to 'unknown' if not provided
        login_username = request.data.get('username')
        login_status = request.data.get('status', 'S')

        # Create a login activity record
        login_activity = UserLoginActivity.objects.create(
            login_IP=login_ip,
            login_datetime=timezone.now(),
            login_username=login_username,
            status=login_status,
            user_agent_info=user_agent_info  # Ensure this is not null
        )

        serializer = UserLoginActivitySerializer(login_activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserActivityView(APIView):
    def get(self, request, username):
        # Fetch the user's activity details
        user_activities = UserActivity1.objects.filter(user__username=username).order_by('-date')
        
        if user_activities.exists():
            serializer = UserActivitySerializer(user_activities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No activity found for this user'}, status=status.HTTP_404_NOT_FOUND)