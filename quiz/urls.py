from django.urls import path
from .views import QuizListAPIView, QuizDetailAPIView, QuizDataAPIView,QuizResultAPIView,GenerateQuizQuestionsAPIView

urlpatterns = [
    path('', QuizListAPIView.as_view(), name="quiz_list_api"),  # List of quizzes
    path('<pk>/', QuizDetailAPIView.as_view(), name="quiz_detail_api"),  # Quiz details
    path('<pk>/data/', QuizDataAPIView.as_view(), name="quiz_data_api"),  # Fetch quiz questions and answers
    path('<pk>/save/', QuizResultAPIView.as_view(), name="quiz_result_api"),
    path('<pk>/generate/', GenerateQuizQuestionsAPIView.as_view(), name="quiz_generate_api"),  # Generate questions and answers using AI
]
