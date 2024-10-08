from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import Student, CustomUser
from rest_framework.test import APITestCase
from curriculum.models import Lesson, Standard, Subject,School
from unittest.mock import patch

class StandardListAPITestCase(APITestCase):
    def setUp(self):
        # Set up the API client
        self.client = APIClient()

        # Create test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )

        # Create the user profile
        self.profile1 = Student.objects.create(
            user=self.user,
            grade=5,
            school="Sparsh Global School,Greater Noida"
        )

        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        
    def test_standard_list_valid_school_in_list1(self):
        """
        Test for a user whose school is in list1, and valid grades should be returned.
        """
        url = reverse('curriculum:standard_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('grades', response.data)
        self.assertIn('standards', response.data)

        # Check if the correct grades were returned
        expected_grades = list(range(1, 10))
        self.assertEqual(response.data['grades'], expected_grades)

    def test_standard_list_valid_school_in_list2(self):
        """
        Test for a user whose school is in list2, and valid grades should be returned.
        """
        self.profile1.school = "Vivekanand School,Anand Vihar"
        self.profile1.save()

        url = reverse('curriculum:standard_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_standard_list_invalid_user_profile(self):
        """
        Test for a user who does not have a valid profile.
        """
        # Create a new user without a profile
        new_user = CustomUser.objects.create_user(username='nouserprofile', password='password')
        self.client.force_authenticate(user=new_user)

        url = reverse('curriculum:standard_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User profile does not exist.')

    def test_standard_list_no_school(self):
        self.profile1.school = "Unknown School"
        self.profile1.save()

        url = reverse('curriculum:standard_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the grade is checked as an integer
        self.assertEqual(response.data['grades'], [int(self.profile1.grade)])

    def tearDown(self):
        self.client.logout()
        
class SubjectListAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()  # Use APIClient for API tests

        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )
    
        # Authenticate the user for tests
        self.client.force_authenticate(user=self.user)
        
        # Create a test school
        self.school = School.objects.create(name="Test School")

        # Create a test grade (standard)
        self.standard = Standard.objects.create(name="5th Grade", slug='5th-grade')

        # Create a test student profile for the user
        self.student = Student.objects.create(user=self.user, school=self.school, grade=self.standard)

        # Create subjects related to the school and grade with unique subject_ids
        self.subject1 = Subject.objects.create(subject_id="MATH_001", name="Mathematics", slug="mathematics", standard=self.standard)
        self.subject2 = Subject.objects.create(subject_id="SCI_001", name="Science", slug="science", standard=self.standard)

        # Associate subjects with the school
        self.subject1.schools.add(self.school)
        self.subject2.schools.add(self.school)

        # API URL
        self.url = reverse('curriculum:subject_list',kwargs={'slug': self.standard.slug})

    def test_get_subjects_success(self):
        """Test successful retrieval of subjects."""
        response = self.client.get(self.url)
        subject_names = [subject['name'] for subject in response.data['filtered_subjects']]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Mathematics', subject_names)
        self.assertIn('Science', subject_names)

    def test_get_subjects_unauthenticated(self):
        """Test that unauthenticated access returns 403 Forbidden."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_profile_does_not_exist(self):
        """Test when the student profile does not exist for the user."""
        # Remove the student profile
        self.student.delete()
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "User profile does not exist.")

    def test_school_does_not_exist(self):
        """Test when the school does not exist."""
        # Remove the school
        self.school.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "School does not exist.")

    def test_unexpected_exception(self):
        """Test unexpected exception handling."""
        # Patch the 'Student.objects.get' method to raise an exception
        with patch('curriculum.models.Student.objects.get') as mock_get:
            mock_get.side_effect = Exception("Unexpected Error")
            
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['error'], "Unexpected Error")
            
class LessonListAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )
        cls.school = School.objects.create(name="Test School")
        cls.standard = Standard.objects.create(name="5th Grade", slug="5th-grade")

        # Ensure the subject is linked to the standard
        cls.subject = Subject.objects.create(name="Mathematics", standard=cls.standard)
        cls.subject.slug = "mathematics"  # Explicitly set the slug
        cls.subject.save()  # Ensure it is saved
        print(f"Created Standard: {cls.standard}, Slug: {cls.standard.slug}")
        print(f"Created Subject: {cls.subject}, Slug: {cls.subject.slug}")

        cls.student = Student.objects.create(user=cls.user, school=cls.school, grade=cls.standard)

        cls.lesson1 = Lesson.objects.create(
            lesson_id="lesson_1",
            name="Lesson 1",
            subject=cls.subject,
            Standard=cls.standard,
            position="1"
        )
        cls.lesson2 = Lesson.objects.create(
            lesson_id="lesson_2",
            name="Lesson 2",
            subject=cls.subject,
            Standard=cls.standard,
            position="2"
        )

        cls.lesson1.schools.add(cls.school)
        cls.lesson2.schools.add(cls.school)

        cls.url = reverse('curriculum:lesson_list', kwargs={'standard': '5th-grade', 'slug': 'mathematics'})


        
    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_get_lessons_success(self):
        """Test successful retrieval of lessons."""
        print("Created Standard:", self.standard)
        print("Created Subject:", self.subject)
        print("Subject Slug:", self.subject.slug)  # Print the slug for verification
        
        response = self.client.get(self.url)
        print(response.status_code)  # Add this line to check the status code
        print(response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lessons_unauthenticated(self):
        """Test that unauthenticated access returns 403 Forbidden."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_profile_does_not_exist(self):
        """Test when the student profile does not exist for the user."""
        self.student.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "User profile does not exist.")

    def test_school_does_not_exist(self):
        """Test when the school does not exist."""
        self.school.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "School does not exist.")

    def test_subject_does_not_exist(self):
        """Test when the subject does not exist."""
        # Delete the subject
        self.subject.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Subject does not exist.")

    def test_unexpected_exception(self):
        """Test unexpected exception handling."""
        with patch('curriculum.models.Student.objects.get') as mock_get:
            mock_get.side_effect = Exception("Unexpected Error")
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['error'], "Unexpected Error")
            
            
class LessonDetailAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = CustomUser.objects.create_user(
            username='testuser', 
            password='password',
            email='testuser@example.com'
        )

        cls.school = School.objects.create(name="Test School")
        cls.standard = Standard.objects.create(name="5th Grade", slug="5th-grade")
        cls.subject = Subject.objects.create(name="Mathematics", slug="mathematics", standard=cls.standard)

        cls.lesson = Lesson.objects.create(
            lesson_id="lesson_1",
            name="Lesson 1",
            slug="lesson-1",
            Standard=cls.standard,
            subject=cls.subject,
            position="1",
            tutorial_video="http://example.com/video",
            hint=None,
            quiz="http://example.com/quiz",
            content="http://example.com/content",
            editor="http://example.com/editor",
            display_on_frontend=True,
            mark_as_completed=True
        )

        cls.url = reverse('curriculum:lesson_detail', kwargs={
        'standard': cls.standard.slug,
        'subject': cls.subject.slug,
        'slug': cls.lesson.slug
        })

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_get_lesson_detail_success(self):
        """Test retrieving lesson detail successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lesson']['name'], self.lesson.name)

    def test_lesson_not_found(self):
        """Test lesson not found scenario."""
        url = reverse('curriculum:lesson_detail', kwargs={
            'standard': self.standard.slug,
            'subject': self.subject.slug,
            'slug': 'non-existent-lesson'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Test that unauthenticated access is forbidden."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_standard_not_found(self):
        """Test standard slug not found."""
        url = reverse('curriculum:lesson_detail', kwargs={
            'standard': 'non-existent-standard',
            'subject': self.subject.slug,
            'slug': self.lesson.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subject_not_found(self):
        """Test subject slug not found."""
        url = reverse('curriculum:lesson_detail', kwargs={
            'standard': self.standard.slug,
            'subject': 'non-existent-subject',
            'slug': self.lesson.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)