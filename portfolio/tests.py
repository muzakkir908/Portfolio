from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Skill
from .forms import ProjectForm, SkillForm, ContactForm

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
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
        data = {
            'name': 'Test User',
            'email': 'test@test.com',
            'message': 'Test Message'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)

    def test_project_create(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'title': 'New Project',
            'description': 'New Description'
        }
        response = self.client.post(reverse('project_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='New Project').exists())

    def test_project_edit(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'title': 'Updated Project',
            'description': 'Updated Description'
        }
        response = self.client.post(
            reverse('project_edit', kwargs={'pk': self.project.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project')

    def test_project_delete(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('project_delete', kwargs={'pk': self.project.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_skill_create(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'name': 'Django',
            'category': 'Programming'
        }
        response = self.client.post(reverse('skill_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Skill.objects.filter(name='Django').exists())

    def test_skill_edit(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'name': 'Updated Skill',
            'category': 'Programming'
        }
        response = self.client.post(
            reverse('skill_edit', kwargs={'pk': self.skill.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, 'Updated Skill')

    def test_skill_delete(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('skill_delete', kwargs={'pk': self.skill.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

class FormTests(TestCase):
    def test_project_form(self):
        form = ProjectForm(data={
            'title': 'Test Project',
            'description': 'Test Description'
        })
        self.assertTrue(form.is_valid())

    def test_skill_form(self):
        form = SkillForm(data={
            'name': 'Python',
            'category': 'Programming'
        })
        self.assertTrue(form.is_valid())

    def test_contact_form(self):
        form = ContactForm(data={
            'name': 'Test User',
            'email': 'test@test.com',
            'message': 'Test Message'
        })
        self.assertTrue(form.is_valid())