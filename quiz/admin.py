from django.contrib import admin
from .models import Quiz, Question, Answer,Result
from user.models import CustomUser

# Inline admin for answers
class AnswerInLine(admin.TabularInline):
    model = Answer

    # Override get_queryset to filter answers based on the quiz's questions created by the logged-in user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all answers
        # Filter answers by questions related to quizzes created by the logged-in user
        return qs.filter(question__quiz__created_by=request.user)

# Admin for question model with an inline for answers
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]
    list_display = ['question_number', 'question']
    list_filter = ['quiz']

    # Override get_queryset to filter questions based on the quizzes owned by the logged-in user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all questions
        # Filter questions by quizzes created by the logged-in user
        return qs.filter(quiz__created_by=request.user)

# Admin for quiz model that shows only quizzes created by the logged-in mentor
class QuizAdmin(admin.ModelAdmin):
    list_display = ['quiz_name', 'topic', 'grade','created_by']
    list_filter = ['schools']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all quizzes
        return qs.filter(created_by=request.user)

    # Automatically set the creator of the quiz
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new object
            obj.created_by = request.user  # Set the creator to the logged-in user
        super().save_model(request, obj, form, change)

    # Filter user dropdown to show only teachers
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":  # Assuming 'created_by' is the field
            kwargs["queryset"] = CustomUser.objects.filter(role="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Result)
