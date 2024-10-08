from rest_framework import serializers
from .models import Quiz, Question, Answer,Result

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, source='get_answers')

    class Meta:
        model = Question
        fields = "__all__"

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='get_questions')

    class Meta:
        model = Quiz
        fields = "__all__"
        
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields="__all__"
