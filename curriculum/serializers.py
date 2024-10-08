from rest_framework import serializers
from .models import Standard,Lesson,Subject

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