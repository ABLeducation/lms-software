from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student,UserLoginActivity,Teacher,School
from rest_framework.exceptions import NotFound
from .serializers import TeacherSerializer

class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            teacher_obj = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            raise NotFound(detail="Teacher record not found for this user.")

        # Serialize the teacher's profile
        teacher_profile = TeacherSerializer(teacher_obj)

        return Response({
            "profile": teacher_profile.data,
        })