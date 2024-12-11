from rest_framework import serializers
from .models import Standard,Lesson,Subject,LessonAccessReport

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ['name', 'slug']
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields="__all__"
        
class LessonAccessReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAccessReport
        fields = [
            'user', 'lesson', 'video_time_spent', 'hint_time_spent', 
            'content_time_spent', 'is_video_completed', 'is_hint_used',
            'is_content_completed', 'accessed_at', 'updated_at'
        ]