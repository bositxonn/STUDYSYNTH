from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course

class CourseAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course_data = {
            'title': 'Test Course',
            'description': 'A very fine test course.',
            'category': 'Testing'
        }
        self.course = Course.objects.create(**self.course_data)
        self.url = reverse('courses:course-list')

    def test_list_courses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course(self):
        new_course_data = {
            'title': 'New Course',
            'description': 'Description here',
            'category': 'New Category'
        }
        response = self.client.post(self.url, new_course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        url = reverse('courses:course-detail', args=[self.course.id])
        update_data = {'title': 'Updated Title', 'description': 'Updated Description', 'category': 'Updated Category'}
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Title')

    def test_delete_course(self):
        url = reverse('courses:course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
