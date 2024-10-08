from django.db import models
from user.models import *
from curriculum.models import School

class Quiz(models.Model):
    quiz_name=models.CharField(max_length=150)
    topic=models.CharField(max_length=150)
    grade=models.CharField(max_length=100, default=0)
    no_of_questions=models.IntegerField()
    time=models.IntegerField(help_text="duration of the quiz in minutes")
    passing_score_percentage=models.IntegerField(help_text="required score to pass in %")
    schools = models.ManyToManyField(School)
    date=models.DateTimeField(null=True)
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)  
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_quizzes',blank=True,null=True)

    def __str__(self):
        return f"{self.quiz_name}-{self.topic}"
    
    def get_questions(self):
        return self.question_set.all()
    
    class Meta:
        verbose_name_plural='Quizzes'

class Question(models.Model):
    question_number=models.IntegerField()
    question=models.CharField(max_length=500)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.question)
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    answer=models.CharField(max_length=500)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer-{self.answer},Correct-{self.correct}"
    
class Result(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score=models.FloatField()
    date_attempted = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True) 

    def __str__(self):
        return str(self.user)