# portfolio/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .models import Project, Skill
from .forms import ProjectForm, ContactForm, SkillForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('home')


# Home view
def home(request):
    return render(request, 'portfolio/home.html')

# Contact view
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Prepare the email content
            subject = f'New message from {name}'
            message_body = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
            recipient = 'muzakkir13072000@gmail.com'

            try:
                # Send the email
                send_mail(subject, message_body, email, [recipient])
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')
            except Exception as e:
                messages.error(request, "There was an error sending your message. Please try again later.")
                print(e)

    else:
        form = ContactForm()

    contact_details = {
        'email': 'muzakkir13072000@gmail.com',
        'phone': '0894172794',
        'linkedin': 'https://linkedin.com/in/Muzakkir-Pathan'
    }

    return render(request, 'portfolio/contact.html', {'form': form, 'contact_details': contact_details})

# Projects Views
def projects(request):
    all_projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': all_projects})

@staff_member_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project created successfully!")
            return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'portfolio/project_form.html', {'form': form, 'form_title': 'Create Project'})

@staff_member_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'portfolio/project_form.html', {'form': form, 'form_title': 'Edit Project'})

@staff_member_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('projects')
    return render(request, 'portfolio/project_confirm_delete.html', {'project': project})

# Skills Views
def skill_list(request):
    skills = Skill.objects.all().order_by('category', 'name')
    return render(request, 'portfolio/skills.html', {'skills': skills})

@staff_member_required
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill created successfully!")
            return redirect('skill_list')
    else:
        form = SkillForm()
    return render(request, 'portfolio/skill_form.html', {'form': form})

@staff_member_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect('skill_list')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'portfolio/skill_form.html', {'form': form})

@staff_member_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully!")
        return redirect('skill_list')
    return render(request, 'portfolio/skill_confirm_delete.html', {'skill': skill})

