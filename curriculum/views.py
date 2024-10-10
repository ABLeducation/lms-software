from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Standard
from .serializers import SubjectSerializer
from .models import Student,School,Subject,Lesson
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .serializers import LessonSerializer
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework.generics import ListAPIView

class StandardListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_profile = Student.objects.get(user=request.user)
            grade = user_profile.grade
            school = user_profile.school

            list1 = ["Sparsh Global School,Greater Noida", "JP International School,Greater Noida", "SPS,Sonipat"]
            list2 = ["Vivekanand School"]

            if school in list1:
                valid_grades = list(range(1, 10))
            elif school in list2:
                valid_grades = list(range(6, 10))
            else:
                valid_grades = [int(grade)] 

            return Response({
                'grades': valid_grades, 
                'standards': Standard.objects.values()
            }, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"error": "User profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class SubjectListAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, slug=None):
        try:
            # Retrieve the user's profile
            user_profile = Student.objects.get(user=request.user)
            school = School.objects.get(name=user_profile.school)
            grade = user_profile.grade
            
            # Filter subjects based on the user's school and grade
            filtered_subjects = Subject.objects.filter(schools=school, standard__slug=slug)

            if not filtered_subjects.exists():
                return Response({'message': 'No subjects found for the given school and grade.'}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the filtered subjects
            subjects_data = SubjectSerializer(filtered_subjects, many=True).data  # Assuming a SubjectSerializer exists
            
            return Response({'filtered_subjects': subjects_data}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'error': "User profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except School.DoesNotExist:
            return Response({'error': "School does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LessonListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, standard, slug):
        try:
            user_profile = Student.objects.get(user=request.user)
            school = School.objects.get(name=user_profile.school) 
            standard_obj = Standard.objects.get(slug=standard)
            subject = Subject.objects.get(slug=slug)

            filtered_lessons = Lesson.objects.filter(schools=school, subject=subject)

            serializer = LessonSerializer(filtered_lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"error": "User profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except School.DoesNotExist:
            return Response({"error": "School does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Standard.DoesNotExist:
            return Response({"error": "Standard does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Subject.DoesNotExist:
            return Response({"error": "Subject does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, standard, subject, slug):
        lesson = get_object_or_404(
            Lesson, 
            slug=slug, 
            Standard__slug=standard, 
            subject__slug=subject
        )

        # Serialize the lesson details
        lesson_data = {
            'id': lesson.id,
            'name': lesson.name,
            'lesson_id': lesson.lesson_id,
            'standard': lesson.Standard.name,
            'subject': lesson.subject.name,
            'position': lesson.position,
            'tutorial_video': lesson.tutorial_video,
            'hint': lesson.hint.url if lesson.hint else None,
            'quiz': lesson.quiz,
            'content': lesson.content,
            'editor': lesson.editor,
            'display_on_frontend': lesson.display_on_frontend,
            'mark_as_cpmpleted':lesson.mark_as_completed
        }

        return Response({'lesson': lesson_data}, status=status.HTTP_200_OK)