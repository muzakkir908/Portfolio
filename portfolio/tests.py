from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Skill
from .forms import ProjectForm, SkillForm, ContactForm
import os

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Use environment variables for test credentials
        test_user = os.environ.get('TEST_ADMIN_USER', 'testadmin')
        test_email = os.environ.get('TEST_ADMIN_EMAIL', 'test@example.com')
        test_password = os.environ.get('TEST_ADMIN_PASSWORD', 'test_password_123')
        
        self.user = User.objects.create_superuser(
            username=test_user,
            email=test_email,
            password=test_password
        )
        self.test_password = test_password
        
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description'
        )
        
        self.skill = Skill.objects.create(
            name='Python',
            category='Programming'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/home.html')

    def test_projects_view(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/projects.html')
        self.assertContains(response, 'Test Project')

    def test_skills_view(self):
        response = self.client.get(reverse('skill_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/skills.html')
        self.assertContains(response, 'Python')

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/contact.html')

    def test_contact_view_post(self):
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test Message'
        }
        response = self.client.post(reverse('contact'), test_data)
        self.assertEqual(response.status_code, 302)

    def test_project_create(self):
        # Login using saved test password
        self.client.login(
            username=self.user.username,
            password=self.test_password
        )
        test_data = {
            'title': 'New Project',
            'description': 'New Description'
        }
        response = self.client.post(reverse('project_create'), test_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='New Project').exists())

    def test_project_edit(self):
        self.client.login(
            username=self.user.username,
            password=self.test_password
        )
        test_data = {
            'title': 'Updated Project',
            'description': 'Updated Description'
        }
        response = self.client.post(
            reverse('project_edit', kwargs={'pk': self.project.pk}),
            test_data
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project')

    def test_project_delete(self):
        self.client.login(
            username=self.user.username,
            password=self.test_password
        )
        response = self.client.post(
            reverse('project_delete', kwargs={'pk': self.project.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_skill_create(self):
        self.client.login(
            username=self.user.username,
            password=self.test_password
        )
        test_data = {
            'name': 'Django',
            'category': 'Programming'
        }
        response = self.client.post(reverse('skill_create'), test_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Skill.objects.filter(name='Django').exists())

    def test_skill_edit(self):
        self.client.login(
            username=self.user.username,
            password=self.test_password
        )
        test_data = {
            'name': 'Updated Skill',
            'category': 'Programming'
        }
        response = self.client.post(
            reverse('skill_edit', kwargs={'pk': self.skill.pk}),
            test_data
        )
        self.assertEqual(response.status_code, 302)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, 'Updated Skill')

    def test_skill_delete(self):
        self.client.login(
            username=self.user.username,
            password=self.test_password
        )
        response = self.client.post(
            reverse('skill_delete', kwargs={'pk': self.skill.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

class FormTests(TestCase):
    def test_project_form(self):
        test_data = {
            'title': 'Test Project',
            'description': 'Test Description'
        }
        form = ProjectForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_skill_form(self):
        test_data = {
            'name': 'Python',
            'category': 'Programming'
        }
        form = SkillForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_contact_form(self):
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test Message'
        }
        form = ContactForm(data=test_data)
        self.assertTrue(form.is_valid())