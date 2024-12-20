import pytest # type: ignore
from rest_framework import status 
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from user.models import *
from django.utils import timezone
from datetime import date
from curriculum.models import Standard,Subject
from django.core.files.uploadedfile import SimpleUploadedFile
from quiz.models import Quiz,Result
from django.test import TestCase
from io import BytesIO
from django.conf import settings

@pytest.mark.django_db
def test_register_student(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "student1",
            "password": "password123",
            "email": "student1@example.com",
            "role": "student"
        },
        "name": "Student Name",
        "grade": "Grade 5",
        "section": "A",
        "school": "School Name"
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_register_teacher(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "teacher1",
            "password": "password123",
            "email": "teacher1@example.com",
            "role": "teacher"
        },
        "school": "School Name"
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_register_school(client):
    url = reverse('users:register')

    data = {
        "user": {
            "username": "school1",
            "password": "password123",
            "email": "school1@example.com",
            "role": "school"
        },
        "school": "School Name",
        "city": "Noida",
        "state": "UP",
        "country": "India",
        "principal_name": "XYZ",
        "principal_number": "9876543210",
        "principal_email": "principal@example.com", 
        "teacher_coordinator": "Coordinator 1",
        "teacher_coordinator_number": "1234567890",
        "teacher_coordinator_email": "coordinator@example.com", 
        "accountant_number": "1234567890",
        "account_name": "Account Holder",
        "account_email": "accountant@example.com", 
        "geo_location": "28.7041,77.1025",
    }

    # Send POST request with multipart data
    response = client.post(url, data=data, content_type='application/json')

    # Print response content if the status code is not 201
    if response.status_code != status.HTTP_201_CREATED:
        print("Response content:", response.content)

    assert response.status_code == status.HTTP_201_CREATED
    
@pytest.mark.django_db
def test_register_invalid_role(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "invalid1",
            "password": "password123",
            "email": "invalid1@example.com",
            "role": "invalid_role"
        }
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.login_url = reverse('users:login')

    def test_login_with_username(self):
        data = {
            'username_or_email': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_email(self):
        data = {
            'username_or_email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {
            'username_or_email': 'wronguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_missing_password(self):
        data = {
            'username_or_email': 'testuser'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_missing_username_or_email(self):
        data = {
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username_or_email', response.data) 


class UserActivityTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        UserActivity1.objects.create(
            user=self.user,
            date=timezone.now(),
            page_visited='Home',
            time_spent='00:05:00'
        )

    def test_get_user_activity(self):
        url = reverse('users:user-activity', args=['testuser'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class StudentDashboardAPITest(APITestCase):
    
    def setUp(self):
        # Create a user and set them to active for testing
        self.user = CustomUser.objects.create_user(username='student1', password='password123')
        self.user.is_active = True
        self.user.save()

        # Create a Standard
        self.standard = Standard.objects.create(name='8')

        # Create Subjects associated with the Standard
        Subject.objects.create(subject_id="ms", name='Math', standard=self.standard)
        Subject.objects.create(subject_id="sc", name='Science', standard=self.standard)

        # Create a Student associated with the user and the Standard
        self.student = Student.objects.create(user=self.user, grade=self.standard)

        # Create Quizzes associated with the user's grade
        self.quiz1 = Quiz.objects.create(
            no_of_questions=1,
            quiz_name='Math Quiz',
            grade=self.standard,
            start_date=timezone.make_aware(timezone.datetime(2024, 10, 1)),
            end_date=timezone.make_aware(timezone.datetime(2024, 10, 30)),
            time=30,
            passing_score_percentage=70
        )
        self.quiz2 = Quiz.objects.create(
            no_of_questions=1,
            quiz_name='Science Quiz',
            grade=self.standard,
            start_date=timezone.make_aware(timezone.datetime(2024, 10, 1)),
            end_date=timezone.make_aware(timezone.datetime(2024, 10, 30)),
            time=30,
            passing_score_percentage=70
        )

        # Create Results for the quizzes
        self.result1 = Result.objects.create(quiz=self.quiz1, user=self.user, score=85)
        self.result2 = Result.objects.create(quiz=self.quiz2, user=self.user, score=90)

        # Create User Login Activity
        UserLoginActivity.objects.create(login_username=self.user, login_datetime=timezone.now())

    def test_student_dashboard_authenticated(self):
        # Authenticate the user by obtaining a token
        login_url = reverse('users:login')
        login_data = {
            "username_or_email": "student1",
            "password": "password123"
        }
        response = self.client.post(login_url, login_data, format='json')
        
        # Check if login was successful
        print("Login response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Retrieve username from login response
        username = response.data.get("username")
        self.assertEqual(username, self.user.username)

        # Use the username to access the student's dashboard
        dashboard_url = reverse('users:student-dashboard', kwargs={"username": username})
        dashboard_response = self.client.get(dashboard_url)
        self.assertEqual(dashboard_response.status_code, status.HTTP_200_OK)
        
        # Check subjects
        self.assertEqual(len(dashboard_response.data['subjects']), 2)

        # Check if quizzes are retrieved correctly
        self.assertEqual(len(dashboard_response.data['quizzes']), 2)
        self.assertEqual(dashboard_response.data['quizzes'][0]['quiz_name'], 'Math Quiz')
        self.assertEqual(dashboard_response.data['quizzes'][1]['quiz_name'], 'Science Quiz')

        # Check if results are retrieved correctly
        self.assertEqual(len(dashboard_response.data['results']), 2)
        self.assertEqual(dashboard_response.data['results'][0]['score'], 85)
        self.assertEqual(dashboard_response.data['results'][1]['score'], 90)


    def test_student_dashboard_unauthenticated(self):
        # Make the API call without authentication
        dashboard_url = reverse('users:student-dashboard', kwargs={"username": "student1"})
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class StudentProfileUpdateAvatarTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass123")
        # Create a student profile
        self.student = Student.objects.create(
            user=self.user,
            name="Test Student",
            grade="10",
            section="A",
            school="Test School"
        )
        # Set up the client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create dummy avatar files in the media folder
        self.avatar_folder = os.path.join(settings.MEDIA_ROOT, "avatars")
        os.makedirs(self.avatar_folder, exist_ok=True)
        self.avatar_files = [
            "av_1.png", "av_2.png", "av_3.png", "av_4.png", "av_5.png",
        ]
        for avatar in self.avatar_files:
            with open(os.path.join(self.avatar_folder, avatar), "wb") as f:
                f.write(BytesIO(b"Test Image Content").getbuffer())

    def tearDown(self):
        # Clean up the test avatars
        for avatar in self.avatar_files:
            path = os.path.join(self.avatar_folder, avatar)
            if os.path.exists(path):
                os.remove(path)

        if os.path.exists(self.avatar_folder):
            os.rmdir(self.avatar_folder)

    def test_update_avatar_success(self):
        """Test successfully updating the profile picture with a predefined avatar."""
        response = self.client.post(
            f"/student/{self.user.username}/update-avatar/",
            {"avatar_choice": "avatar1"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Profile picture updated successfully.")

        # Verify the profile picture was updated
        self.student.refresh_from_db()
        self.assertTrue(self.student.profile_pic.name.endswith("avatar1.png"))

    def test_update_avatar_invalid_choice(self):
        """Test providing an invalid avatar choice."""
        response = self.client.post(
            f"/student/{self.user.username}/update-avatar/",
            {"avatar_choice": "invalid_avatar"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid avatar choice.")

    def test_update_avatar_missing_file(self):
        """Test updating avatar when the file for the avatar choice is missing."""
        # Remove one of the test avatars to simulate missing file
        os.remove(os.path.join(self.avatar_folder, "av_1.png"))

        response = self.client.post(
            f"/student/{self.user.username}/update-avatar/",
            {"avatar_choice": "avatar1"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Avatar file 'avatar1' not found.")

    def test_unauthorized_update_avatar(self):
        """Test updating avatar without authentication."""
        self.client.logout()
        response = self.client.post(
            f"/student/{self.user.username}/update-avatar/",
            {"avatar_choice": "avatar1"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PasswordResetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='test@example.com')
        self.password_reset_url = reverse('users:password_reset_request')

    def test_password_reset_flow(self):
        # Simulate the 'forgot password' request
        forgot_password_data = {
            "email": self.user.email  # Use 'email' if that's what your view expects
        }
        # Make a POST request to initiate password reset
        response = self.client.post(self.password_reset_url, data=forgot_password_data, format="json")
        # Validate response for successful email send
        self.assertEqual(response.status_code, 200)

    def test_password_reset_with_wrong_email(self):
        # Data with incorrect email
        forgot_password_data = {
            "email": "wrongemail@example.com"
        }
        # Attempt to initiate password reset with the wrong email
        response = self.client.post(self.password_reset_url, data=forgot_password_data, format="json")
        # Validate response for failure due to incorrect email
        self.assertEqual(response.status_code, 400)
        
# class ZoomMeetingPermissionTestCase(APITestCase):

#     def setUp(self):
#         # Create an admin user and a regular user
#         self.admin_user = CustomUser.objects.create_user(
#         username='adminuser', 
#         email='adminuser@example.com', 
#         password='adminpass', 
#         is_staff=True
#         )
#         self.regular_user = CustomUser.objects.create_user(
#             username='regularuser', 
#             email='regularuser@example.com', 
#             password='regularpass', 
#             is_staff=False
#         )
#         # Define URL for Zoom meeting creation endpoint
#         self.zoom_meeting_url = reverse('users:zoom_meeting_create')  # Adjust to your URL name

#     def test_admin_can_create_zoom_meeting(self):
#         # Login as admin
#         self.client.login(username='adminuser', password='adminpass')
        
#         # Define meeting data
#         meeting_data = {
#             "topic": "test",
#             "type": 2,  # 2 for scheduled meetings
#             "start_time": "2021-05-10T12:10:10Z",  # Ensure the date is in the future
#             "duration": 3,  # Use integer type for duration
#             "settings": {
#                 "host_video": True,  # Use boolean type
#                 "participant_video": True,
#                 "join_before_host": True,
#                 "mute_upon_entry": True,
#                 "watermark": True,
#                 "audio": "voip",
#                 "auto_recording": "cloud"
#             }
#         }
#         # Attempt to create a Zoom meeting
#         response = self.client.post(self.zoom_meeting_url, data=meeting_data, format='json')
#         print("Test Response Content:", response.content)
#         print("Response Content:", response.content) 
#         # Assert success response
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('id', response.data)
#         self.assertIn('join_url', response.data)

#     def test_regular_user_cannot_create_zoom_meeting(self):
#         # Login as regular user
#         self.client.login(username='regularuser', password='regularpass')
        
#         # Define meeting data
#         meeting_data = {
#             'topic': 'Test Meeting',
#             'start_time': '2024-12-01T10:00:00Z',
#             'duration': 30,
#             'agenda': 'Test meeting agenda'
#         }
        
#         # Attempt to create a Zoom meeting
#         response = self.client.post(self.zoom_meeting_url, data=meeting_data, format='json')
        
#         # Assert forbidden response
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

        
# class MacroplannerAPITest(APITestCase):

#     def setUp(self):
#         # Create a user for testing
#         self.user = CustomUser.objects.create_user(
#             username='testuser', 
#             email='testuser@example.com', 
#             password='testpassword'
#         )
#         self.create_url = reverse('users:macroplanner_create')  # For POST request
#         self.get_url = reverse('users:macroplanner', args=['Vivekanand School,Delhi'])  # For GET request
        
#     def test_create_macroplanner(self):
#         # Data to be sent in the POST request
#         data = {
#             "user": self.user.id,
#             "grade": "Grade 10",
#             "school": "Vivekanand School,Delhi",
#             "macroplanner": None  # Simulate file upload (set to None for now)
#         }

#         # Mock a file upload by using Django's temporary uploaded file helper
#         with open('testfile.txt', 'w') as f:
#             f.write('Test Macroplanner content')

#         with open('testfile.txt', 'rb') as fp:
#             data['macroplanner'] = fp
            
#             # Send the post request
#             response = self.client.post(self.create_url, data, format='multipart')

#         # Check that the status code is 201 Created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # Verify the response data contains the created macroplanner
#         self.assertEqual(response.data['grade'], 'Grade 10')
#         self.assertEqual(response.data['school'], 'Vivekanand School,Delhi')

#     def test_get_macroplanner_for_school(self):
#         # Create a macroplanner entry for the school
#         Macroplanner.objects.create(
#             user=self.user, 
#             grade='Grade 9', 
#             school='Vivekanand School,Delhi',
#             macroplanner='macroplanner/sample.pdf'
#         )

#         # Send a get request to retrieve the macroplanner for the school
#         response = self.client.get(self.get_url)

#         # Check that the status code is 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Verify the retrieved data
#         self.assertEqual(len(response.data), 1)  # Only one macroplanner for the school
#         self.assertEqual(response.data[0]['grade'], 'Grade 9')

#     def test_get_macroplanner_not_found(self):
#         # Test with a school name that has no macroplanner
#         response = self.client.get(reverse('users:macroplanner', args=['Nonexistent School']))

#         # Check that the status code is 404 Not Found
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['error'], 'Macroplanner not available for this school')
        
# class MicroplannerAPITest(APITestCase):

#     def setUp(self):
#         # Create a user for testing
#         self.user = CustomUser.objects.create_user(
#             username='testuser', 
#             email='testuser@example.com', 
#             password='testpassword',
#         )
#         self.create_url = reverse('users:microplanner-create')  # URL for POST request
#         self.get_url = reverse('users:microplanner', args=['Vivekanand School, Delhi'])  # URL for GET request by school name
        
#     def test_create_microplanner(self):
#         # Data for the POST request
#         data = {
#             "user": self.user.id,
#             "month": "January",
#             "school": "Vivekanand School,Delhi",
#         }

#         # Create a mock file
#         with open('testfile.txt', 'w') as f:
#             f.write('Test Microplanner content')

#         with open('testfile.txt', 'rb') as fp:
#             data['microplanner'] = fp

#             # Send the POST request to create a microplanner
#             response = self.client.post(self.create_url, data, format='multipart')

#         # Print response data for debugging
#         print(response.data)

#         # Check for successful creation (HTTP 201 Created)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#     def test_get_microplanner_for_school(self):
#         # Create a Microplanner for the school
#         Microplanner.objects.create(
#             user=self.user, 
#             month='February', 
#             school='Vivekanand School, Delhi',
#             microplanner='microplanner/sample.pdf'
#         )

#         # Send the GET request to retrieve the microplanner by school name
#         response = self.client.get(self.get_url)

#         # Check for successful retrieval (HTTP 200 OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Verify the retrieved data
#         self.assertEqual(len(response.data), 1)  # Only one microplanner should be present
#         self.assertEqual(response.data[0]['month'], 'February')

#     def test_get_microplanner_not_found(self):
#         # Test with a non-existent school
#         response = self.client.get(reverse('users:microplanner', args=['Nonexistent School']))

#         # Check for 404 Not Found
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['error'], 'Microplanner not available for this school')

# class AdvocacyVisitAPITest(APITestCase):
    
#     def setUp(self):
#         self.school_name = 'Vivekanand School,Delhi'
#         self.advocacy_visit = AdvocacyVisit.objects.create(
#             name='John Doe',
#             grade=10,
#             section='A',
#             school=self.school_name,
#             date='2024-09-25',
#             duration='1 hour',
#             topics='Math',
#             topics_microplanner=False,
#             classroom_management=5,
#             content_delievery=4,
#             student_teacher_relation=3,
#             dresscode=2,
#             handling_comm=4,
#             Regularity=5,
#             Punctuality=4,
#             daily_report=5,
#             daily_progress_sheet=4,
#             overall_behaviour=5,
#             next_month_microplanner=4,
#             kreativityshow=5,
#             compiled_report=4,
#             daily_win_sharing=5,
#             photo_video_recording=4,
#             pedagogical_poweress='Excellent',
#             additional_info='N/A',
#             project_taken_club='Math Club',
#             learning_outcomes='Improved scores',
#             competition='Math Olympiad',
#             feedback='Good job',
#             improvement_tips='Practice more',
#             remarks='Well done',
#             name_advocacy='Principal',
#             verified_by=False,
#             gallery='http://example.com/gallery'
#         )

#     def test_create_advocacy_report(self):
#         data = {
#             "name": "Jane Doe",
#             "grade": 10,
#             "section": "B",
#             "school": self.school_name,
#             "date": "2024-09-26",
#             "duration": "2 hours",
#             "topics": "Science",
#             "topics_microplanner": False,
#             "classroom_management": 4,
#             "content_delievery": 5,
#             "student_teacher_relation": 3,
#             "dresscode": 4,
#             "handling_comm": 3,
#             "Regularity": 4,
#             "Punctuality": 5,
#             "daily_report": 4,
#             "daily_progress_sheet": 5,
#             "overall_behaviour": 4,
#             "next_month_microplanner": 3,
#             "kreativityshow": 5,
#             "compiled_report": 4,
#             "daily_win_sharing": 3,
#             "photo_video_recording": 4,
#             "pedagogical_poweress": "Good",
#             "additional_info": "N/A",
#             "project_taken_club": "Science Club",
#             "learning_outcomes": "Better understanding",
#             "competition": "Science Fair",
#             "feedback": "Great",
#             "improvement_tips": "Focus on experiments",
#             "remarks": "Keep it up!",
#             "name_advocacy": "Vice Principal",
#             "verified_by": False,
#             "gallery": "http://example.com/new-gallery"
#         }
#         response = self.client.post('/advocacy-reports/', data)
#         self.assertEqual(response.status_code, 201)  # Expecting HTTP 201 Created

#     def test_create_advocacy_report_invalid(self):
#         data = {
#             "name": "",  
#             "grade": 10,
#             "section": "B",
#             "school": self.school_name,
#             "date": "2024-09-26",
#             "duration": "2 hours",
#             "topics": "Science",
#             "topics_microplanner": False,
#         }
#         response = self.client.post('/advocacy-reports/', data)
#         self.assertEqual(response.status_code, 400
        
        
# class TeacherDashboardAPITest(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.user = CustomUser.objects.create_user(
#             username='teacher1', email='teacher1@example.com', password='password123'
#         )
#         cls.teacher = Teacher.objects.create(
#             user=cls.user,
#             school="Test School",
#             name="Test Teacher",
#             mobile_num="1234567890",
#             subject="Math",
#             designation="Senior Teacher",
#             grades="Grade 10"
#         )

#     def test_teacher_dashboard_authenticated(self):
#         # Authenticate the user
#         self.client.login(username="teacher1", password="password123")

#         # Make the API call
#         response = self.client.get(reverse('users:teacher-dashboard'))

#         # Debugging output
#         print(response.data)  # Print the response for debugging

#         # Assert the response status code and data
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['profile']['name'], "Test Teacher")

#     def test_teacher_dashboard_not_found(self):
#         # Create another user that is not a teacher
#         non_teacher_user = CustomUser.objects.create_user(
#             username='non_teacher', email='non_teacher@example.com', password='password123'
#         )
#         self.client.login(username='non_teacher', password='password123')

#         # Attempt to access the teacher dashboard
#         response = self.client.get(reverse('users:teacher-dashboard'))

#         # Assert the response status code and error message
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['detail'], "Teacher record not found for this user.")
        
        
# class SchoolDashboardAPITest(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.user = CustomUser.objects.create_user(
#             username='school1', email='school1@example.com', password='password123'
#         )
#         cls.school = School.objects.create(
#             user=cls.user,
#             school="Test School",
#             city="Noida",
#             state="UP",
#             country="India",
#             principal_name="XYZ",
#             teacher_coordinator="POP",
#             accountant_number="1234567890",
#             geo_location="",
#         )

#     def test_school_dashboard_authenticated(self):
#         # Authenticate the user
#         self.client.login(username="school1", password="password123")

#         # Make the API call
#         response = self.client.get(reverse('users:school-dashboard'))

#         # Assert the response status code and data
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['profile']['school'], "Test School")

#     def test_school_dashboard_not_found(self):
#         # Create another user that is not a school
#         non_school_user = CustomUser.objects.create_user(
#             username='non_school', email='non_school@example.com', password='password123'
#         )
#         self.client.login(username='non_school', password='password123')

#         # Attempt to access the school dashboard
#         response = self.client.get(reverse('users:school-dashboard'))

#         # Assert the response status code and error message
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['detail'], "School record not found for this user.")