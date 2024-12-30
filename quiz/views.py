from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import QuizSerializer
from .models import Quiz,Question,Answer,Result
from user.models import Student
from curriculum.models import School
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import generate_certificate,generate_questions_and_answers_using_ai
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

class GenerateQuizQuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        questions = generate_questions_and_answers_using_ai(quiz.quiz_name, quiz.no_of_questions, quiz.topic)

        if not questions:
            return Response(
                {"error": "Failed to generate questions using AI. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        for question_data in questions:
            question = Question.objects.create(
                quiz=quiz,
                question=question_data["question"]
            )
            for answer_text in question_data["answers"]:
                Answer.objects.create(
                    question=question,
                    answer=answer_text,
                    correct=(answer_text == question_data["correct"])
                )

        return Response({"message": "Questions generated and saved successfully."}, status=status.HTTP_201_CREATED)


class QuizListAPIView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            # Raise a NotFound exception, which is the appropriate response for missing resources
            raise NotFound('Student profile does not exist.')
        
        student_grade = student.grade
        student_school = student.school
        school = School.objects.get(name__icontains=student_school)

        # Filter quizzes based on the student's grade and school
        return Quiz.objects.filter(grade=student_grade, schools=school)


class QuizDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'pk'
    
class QuizDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        question_data = []
        for q in quiz.get_questions():
            answers = [a.answer for a in q.get_answers()]
            question_data.append({str(q): answers})
        
        return Response({'data': question_data, 'time': quiz.time}) 

@method_decorator(csrf_exempt, name='dispatch')
class QuizResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = request.data
        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.no_of_questions
        results = []
        correct_answer = None

        for question_text, answer_selected in data.items():
            question = Question.objects.get(question=question_text)
            a_selected = answer_selected  # Get the first answer

            if a_selected:
                question_answers = Answer.objects.filter(question=question)
                for a in question_answers:
                    if a_selected == a.answer and a.correct:
                        score += 1
                        correct_answer = a.answer
                results.append({str(question): {"correct_answer": correct_answer, "answered": a_selected}})
            else:
                results.append({str(question): 'not answered'})

        score_ = score * multiplier
        result = Result.objects.create(quiz=quiz, user=user, score=score_)

        # Check if the user passed the quiz
        passed = score_ >= quiz.passing_score_percentage
        certificate_file = generate_certificate(user, quiz, score_, passed, result.date_attempted)
        result.certificate.save(certificate_file.name, certificate_file)

        return Response({"passed": passed, "score": score_, "results": results})