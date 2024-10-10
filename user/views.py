from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import login
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema # type: ignore
from rest_framework import generics
from drf_yasg import openapi # type: ignore
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=SchoolSerializer,  # Use a single serializer
        responses={201: SchoolSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Print the entire data received
        
        user_data = request.data
        # Extract user details from the request
        user_info = user_data.get('user', {})
        
        if not isinstance(user_info, dict):
            return Response({'error': 'Invalid user data format'}, status=status.HTTP_400_BAD_REQUEST)

        role = user_info.get('role')
        print("Role:", role)

        # Prepare data for the correct serializer
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
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: 'Token', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Log out the user
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class UserLoginActivityView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginActivitySerializer,
        responses={201: UserLoginActivitySerializer, 400: 'Bad Request'}
    )
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


class MacroplannerView(generics.GenericAPIView):
    serializer_class = MacroplannerSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('school_name', openapi.IN_QUERY, description="School Name", type=openapi.TYPE_STRING)],
        responses={200: MacroplannerSerializer(many=True), 404: 'Not Found', 400: 'Bad Request'}
    )
    def get(self, request, school_name=None):
        if school_name:
            macroplanner = Macroplanner.objects.filter(school=school_name)
            if macroplanner.exists():
                serializer = MacroplannerSerializer(macroplanner, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Macroplanner not available for this school'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'School name is required'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=MacroplannerSerializer,
        responses={201: MacroplannerSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MicroplannerView(generics.GenericAPIView):
    serializer_class = MicroplannerSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('school_name', openapi.IN_QUERY, description="School Name", type=openapi.TYPE_STRING)],
        responses={200: MicroplannerSerializer(many=True), 404: 'Not Found', 400: 'Bad Request'}
    )
    def get(self, request, school_name=None):
        if school_name:
            microplanner = Microplanner.objects.filter(school=school_name)
            if microplanner.exists():
                serializer = MicroplannerSerializer(microplanner, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Microplanner not available for this school'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'School name is required'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=MicroplannerSerializer,
        responses={201: MicroplannerSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdvocacyVisitView(generics.GenericAPIView):
    serializer_class = AdvocacyVisitSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('school_name', openapi.IN_QUERY, description="School Name", type=openapi.TYPE_STRING)],
        responses={200: AdvocacyVisitSerializer(many=True), 404: 'Not Found', 400: 'Bad Request'}
    )
    def get(self, request, school_name=None):
        if school_name:
            queryset = AdvocacyVisit.objects.filter(school=school_name)
            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Advocacy visit not available for this school'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'School name is required'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=AdvocacyVisitSerializer,
        responses={201: AdvocacyVisitSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)