from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('projects/', views.projects, name='projects'),  # Projects list
    path('projects/new/', views.project_create, name='project_create'),  # Create project
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),  # Edit project
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),  # Delete project
    path('contact/', views.contact_view, name='contact'),  # Contact form view

    # Skills related views
    path('skills/', views.skill_list, name='skill_list'),  # List skills
    path('skills/create/', views.skill_create, name='skill_create'),  # Create new skill
    path('skills/edit/<int:pk>/', views.skill_edit, name='skill_edit'),  # Edit skill
    path('skills/delete/<int:pk>/', views.skill_delete, name='skill_delete'),  # Delete skill

    
]
