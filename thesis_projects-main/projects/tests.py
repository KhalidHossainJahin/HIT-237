from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, project_list, project_details, about
from .models import ProjectItem

class ProjectTests(TestCase):
    def setUp(self):
        self.project = ProjectItem('Test Project', 'Test Description', 'Test Supervisor', '123')

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_project_list_view(self):
        url = reverse('project_list')
        response = self.client.get(url)
        self.assertTrue('projects' in response.context)

    def test_project_details_view(self):
        url = reverse('project_details', kwargs={'title': self.project.title})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_about_view_status_code(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolves_to_view(self):
        resolver = resolve('/')
        self.assertEquals(resolver.func, home)
