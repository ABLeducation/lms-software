from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import School
from rest_framework.exceptions import NotFound
from .serializers import SchoolSerializer

class SchoolDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            school_obj = School.objects.get(user=user)
        except School.DoesNotExist:
            raise NotFound(detail="School record not found for this user.")

        # Serialize the school's profile
        school_profile = SchoolSerializer(school_obj)

        return Response({
            "profile": school_profile.data,
        })
