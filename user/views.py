from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import login
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema # type: ignore
from rest_framework import generics
from drf_yasg import openapi # type: ignore
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import logout
from django.urls import reverse
from rest_framework import viewsets
from .utils.zoom import create_zoom_meeting
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=SchoolSerializer,  # Use a single serializer
        responses={201: SchoolSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        
        user_data = request.data
        # Extract user details from the request
        user_info = user_data.get('user', {})
        
        if not isinstance(user_info, dict):
            return Response({'error': 'Invalid user data format'}, status=status.HTTP_400_BAD_REQUEST)

        role = user_info.get('role')

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
            if not user.is_active:
                return Response(
                    {"error": "Account is not active. Please contact support."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            # Determine the dashboard URL based on user type
            if Student.objects.filter(user=user).exists():
                dashboard_url = reverse('users:student-dashboard', args=[user.username])
            elif Teacher.objects.filter(user=user).exists():
                dashboard_url = reverse('users:teacher-dashboard', args=[user.username])
            else:
                dashboard_url = reverse('users:school-dashboard', args=[user.username])
                
            return Response({
                "token": token.key,
                "username": user.username,
                "dashboard_url": dashboard_url,
                "role":user.role
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    #only for development, have to remove in production
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = CustomUser.objects.get(email=email)
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Send the reset email
                reset_link = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"
                send_mail(
                    subject="Password Reset Request",
                    message=f"Use this link to reset your password: {reset_link}",
                    from_email="content@thinnkware.com",
                    recipient_list=[email],
                    fail_silently=False  # Set to False to raise exceptions for debugging
                )
                return Response({'success': 'Password reset link sent'}, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get('new_password')
            user.set_password(new_password)
            
            user.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
    
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
    
class ZoomMeetingView(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def create(self, request):
        topic = request.data.get("topic")
        start_time = request.data.get("start_time")
        duration = request.data.get("duration")
        host_email = request.data.get("host_email")

        if not all([topic, start_time, duration, host_email]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        zoom_meeting = create_zoom_meeting(topic, start_time, duration, host_email)
        return Response(zoom_meeting, status=status.HTTP_201_CREATED)