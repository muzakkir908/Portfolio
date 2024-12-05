# portfolio/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    path('contact/', views.contact_view, name='contact'),
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/create/', views.skill_create, name='skill_create'),
    path('skills/edit/<int:pk>/', views.skill_edit, name='skill_edit'),
    path('skills/delete/<int:pk>/', views.skill_delete, name='skill_delete'),
    path('export-pdf/', views.export_portfolio_pdf, name='export_pdf'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
]