from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .serializers import StudentSerializer, TeacherSerializer, SchoolSerializer

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
