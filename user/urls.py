# urls.py
from django.urls import path,include
from .views import *
from .StudentView import *
from .TeacherView import *
from .SchoolView import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'student-profile', StudentProfileViewSet, basename='student-profile')

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('login-activity/', UserLoginActivityView.as_view(), name='login-activity'),
    path('user-activity/<str:username>/', UserActivityView.as_view(), name='user-activity'),
    path('macroplanner/', MacroplannerView.as_view(), name='macroplanner_create'),
    path('macroplanner/<str:school_name>/', MacroplannerView.as_view(), name='macroplanner'),
    path('microplanner/', MicroplannerView.as_view(), name='microplanner-create'),
    path('microplanner/<str:school_name>/', MicroplannerView.as_view(), name='microplanner'),
    path('advocacy-reports/<str:school_name>/', AdvocacyVisitView.as_view(), name='advocacy_reports_get'),  # For GET
    path('advocacy-reports/', AdvocacyVisitView.as_view(), name='advocacy_reports_post'),  # For POST
    
    #Student's url
    path('student_dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('', include(router.urls)),
    path('student_notification/', NotificationAPIView.as_view(), name='student-notification'),
    
    #Teacher's url
    path('teacher_dashboard/', TeacherDashboardView.as_view(), name='teacher-dashboard'),
    
    #School's url
    path('school_dashboard/', SchoolDashboardView.as_view(), name='school-dashboard'),
]