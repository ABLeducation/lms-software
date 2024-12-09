from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from curriculum.serializers import SubjectSerializer
from curriculum.models import Standard,Subject
from .models import Student,UserLoginActivity,NotificationStudent,CustomUser,UserActivity1
from rest_framework.exceptions import NotFound
from .serializers import StudentSerializer,NotificationStudentSerializer,UserLoginActivitySerializer,UserActivitySerializer
from quiz.models import Quiz,Result
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from quiz.serializers import QuizSerializer,ResultSerializer
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.db.models import OuterRef, Subquery
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
import base64

class StudentDashboardView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        # Get username from URL parameters
        username = self.kwargs.get('username')
        try:
            # Fetch the student using the provided username
            user = CustomUser.objects.get(username=username)
            student_obj = Student.objects.get(user=user)
            grade = student_obj.grade
        except CustomUser.DoesNotExist:
            raise NotFound(detail=f"User with username '{username}' does not exist.")
        except Student.DoesNotExist:
            raise NotFound(detail="Student record not found for this user.")

        try:
            # Fetch the corresponding Standard object
            student_grade = Standard.objects.get(name=grade)
        except Standard.DoesNotExist:
            raise NotFound(detail=f"Standard matching grade '{grade}' does not exist.")

        # Fetch subjects related to the student's grade
        return Subject.objects.filter(standard=student_grade)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Get username from URL parameters
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)

        # Serialize the student's profile
        student_profile = StudentSerializer(Student.objects.get(user=user), context={'request': request})
        logs = UserLoginActivity.objects.filter(login_username=user).count()

        # Fetch quizzes related to the student's grade
        student_obj = Student.objects.get(user=user)
        quizzes = Quiz.objects.filter(grade=student_obj.grade)
        quiz_serializer = QuizSerializer(quizzes, many=True)

        results = Result.objects.filter(user=user, certificate__isnull=False)
        result_serializer = ResultSerializer(results, many=True)

        return Response({
            "profile": student_profile.data,
            "total_subjects": queryset.count(),
            "subjects": serializer.data,
            "login_count": logs,
            "quizzes": quiz_serializer.data,
            "results": result_serializer.data
        })

        
class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    # Use 'username' for lookups, but filter through the related 'user' field
    lookup_field = 'user__username'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()  # For schema generation views
        else:
            # Filter by the 'user__username' from the URL, or use the logged-in user's username
            username = self.kwargs.get('user__username', self.request.user.username)
            return Student.objects.filter(user__username=username)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        non_editable_fields = ['username', 'email', 'grade', 'section', 'school']
        for field in non_editable_fields:
            data.pop(field, None)  # Remove non-editable fields if present in the request data

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


    @action(detail=False, methods=['post'], url_path='update-password')
    def update_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Check if the old password is correct
        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()
        
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='update-avatar')
    def update_avatar(self, request, user__username=None):
        instance = self.get_object()
        avatar_choice = request.data.get('avatar_choice')  # Expect the avatar name/key
        
        # Define predefined avatar options (add more as needed)
        predefined_avatars = {
            "avatar1": os.path.join(settings.MEDIA_ROOT, "avatars/av_1.png"),
            "avatar2": os.path.join(settings.MEDIA_ROOT, "avatars/av_2.png"),
            "avatar3": os.path.join(settings.MEDIA_ROOT, "avatars/av_3.png"),
            "avatar4": os.path.join(settings.MEDIA_ROOT, "avatars/av_4.png"),
            "avatar5": os.path.join(settings.MEDIA_ROOT, "avatars/av_5.png"),
            "avatar6": os.path.join(settings.MEDIA_ROOT, "avatars/av_6.png"),
            "avatar7": os.path.join(settings.MEDIA_ROOT, "avatars/av_7.png"),
            "avatar8": os.path.join(settings.MEDIA_ROOT, "avatars/av_8.png"),
            "avatar9": os.path.join(settings.MEDIA_ROOT, "avatars/av_9.png"),
            "avatar10": os.path.join(settings.MEDIA_ROOT, "avatars/av_10.png"),
            "avatar11": os.path.join(settings.MEDIA_ROOT, "avatars/av_11.png"),
            "avatar12": os.path.join(settings.MEDIA_ROOT, "avatars/av_12.png"),
            "avatar13": os.path.join(settings.MEDIA_ROOT, "avatars/av_13.png"),
            "avatar14": os.path.join(settings.MEDIA_ROOT, "avatars/av_14.png"),
            "avatar15": os.path.join(settings.MEDIA_ROOT, "avatars/av_15.png"),
        }

        if avatar_choice not in predefined_avatars:
            return Response({"detail": "Invalid avatar choice."}, status=status.HTTP_400_BAD_REQUEST)

        avatar_path = predefined_avatars[avatar_choice]
        if not os.path.exists(avatar_path):
            return Response({"detail": f"Avatar file '{avatar_choice}' not found."}, status=status.HTTP_404_NOT_FOUND)

        with open(avatar_path, "rb") as avatar_file:
            avatar_content = avatar_file.read()

        instance.profile_pic.save(f"{avatar_choice}.png", ContentFile(avatar_content))
        instance.save()

        return Response({"detail": "Profile picture updated successfully."}, status=status.HTTP_200_OK)
    

class NotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            # Get the student profile linked to the logged-in user
            student = Student.objects.get(user=request.user)
            
            # Retrieve the notifications for the student and order them by most recent
            notifications = NotificationStudent.objects.filter(student_id=student).order_by('-id')
            
            # Serialize the notifications
            serializer = NotificationStudentSerializer(notifications, many=True)
            
            # Return the serialized data as a response
            return Response({'notifications': serializer.data}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'error': "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        

class LeaderAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        try:
            student_obj=Student.objects.get(user=request.user)
            school=student_obj.school
            grade=student_obj.grade
        
            student_result=Result.objects.filter(user=request.user).values('score').first()
            student_score=student_result['score'] if student_result else 0
            
            # Determine the rank of the student within their grade and school
            if student_score > 0:
                student_rank=Result.objects.filter(user__student__school=school, 
                                                   user__student__grade=grade,
                                                   score__gt=student_score).count() + 1
            else:
                student_rank=None
                
            # Retrieve the maximum score across all students in the school
            max_student_score = Result.objects.filter(
                user__student__school=school
            ).aggregate(Max('score'))['score__max']
            
            # Get the highest-ranking student within the same grade and school
            grade_leaders = Result.objects.filter(
                user__student__school=school,
                user__student__grade=grade
            ).order_by('-score').first() or None

            # Get the top 5 students overall in the school
            overall_leaders = Result.objects.filter(
                user__student__school=school
            ).order_by('-score')[:5] or None
            
            leaderboard_data={
                "student_rank":student_rank,
                "student_score":student_score,
                "max_student_score":max_student_score,
                "grade_leaders":{
                    "user":grade_leaders.user.username if grade_leaders else None,
                    "score":grade_leaders.score if grade_leaders else None
                },
                "overall_leaders":[
                    {
                        'user': result.user.username,
                        'score': result.score
                    } for result in overall_leaders
                ]
            }
            return Response(leaderboard_data, status=status.HTTP_200_OK)
            
        except Student.DoesNotExist:
            return Response({'error': "Student profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
class StudentLoginActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        try:
            student_profile = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response(
                {"message": "You do not have permission to view this page."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Prepare subquery to get the latest login datetime for the logged-in user
        latest_login_subquery = UserLoginActivity.objects.filter(
            login_username=OuterRef('login_username')
        ).order_by('-login_datetime').values('login_datetime')[:1]

        # Fetch latest login activities for the logged-in user
        latest_login_activities = UserLoginActivity.objects.filter(
            login_username=user.username,
            login_datetime=Subquery(latest_login_subquery)
        ).distinct().order_by('-login_datetime')

        # Serialize the login activities
        serializer = UserLoginActivitySerializer(latest_login_activities, many=True)

        # Include user ID in the response data
        activities_with_user_id = [
            {
                **activity,
                'user_id': CustomUser.objects.get(username=activity['login_username']).id
            }
            for activity in serializer.data
        ]

        response_data = {
            "activities_with_user_id": activities_with_user_id,
            "student_profile": {
                "name": student_profile.name,
                "school": student_profile.school,
                "grade": student_profile.grade,
                "section": student_profile.section,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)            
    
class UserActivityView(APIView):
    def get(self, request, username):
        # Fetch the user's activity details
        user_activities = UserActivity1.objects.filter(user__username=username).order_by('-date')
        
        if user_activities.exists():
            serializer = UserActivitySerializer(user_activities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No activity found for this user'}, status=status.HTTP_404_NOT_FOUND)                         