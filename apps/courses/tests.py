from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Field, Category, Lesson, Quiz, Question


class CourseAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.field = Field.objects.create(name='IT', slug='it-test')
        self.category = Category.objects.create(field=self.field, name='Testing', slug='testing')
        self.course_data = {
            'title': 'Test Course',
            'description': 'A very fine test course.',
            'category': self.category.id
        }
        self.course = Course.objects.create(
            title=self.course_data['title'],
            description=self.course_data['description'],
            category=self.category
        )
        self.url = reverse('courses:course-list')

    def test_list_courses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course(self):
        new_course_data = {
            'title': 'New Course',
            'description': 'Description here',
            'category': self.category.id
        }
        response = self.client.post(self.url, new_course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        url = reverse('courses:course-detail', args=[self.course.id])
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'category': self.category.id
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Title')

    def test_delete_course(self):
        url = reverse('courses:course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class FrontendFlowTests(TestCase):
    """End-to-end tests of the rendered HTML views."""

    def setUp(self):
        self.client = Client()
        self.field = Field.objects.create(name='IT', slug='it-fe-test')
        self.category = Category.objects.create(field=self.field, name='Python', slug='python-fe')
        self.course = Course.objects.create(title='Python Basics', description='Learn Python', category=self.category)
        self.lesson = Lesson.objects.create(course=self.course, title='Lesson 1', video_url='https://vimeo.com/1', order=1)
        self.quiz = Quiz.objects.create(lesson=self.lesson, title='Quiz 1', passing_score=100)
        Question.objects.create(quiz=self.quiz, text='What is 2+2?', option_a='3', option_b='4', correct_option='B')
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Basics')

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_requires_no_login(self):
        response = self.client.get(reverse('course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Basics')

    def test_lesson_requires_login(self):
        # Without login → should redirect
        response = self.client.get(reverse('lesson-detail', args=[self.lesson.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_quiz_submit_scores_user(self):
        # Superusers bypass paywall
        admin = User.objects.create_superuser('admin_test', 'a@a.com', 'adminpass')
        self.client.login(username='admin_test', password='adminpass')
        response = self.client.post(
            reverse('quiz-detail', args=[self.quiz.id]),
            {f'q_{self.quiz.questions.first().id}': 'B'}
        )
        self.assertRedirects(response, reverse('lesson-detail', args=[self.lesson.id]))
