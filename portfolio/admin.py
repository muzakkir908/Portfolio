# portfolio/admin.py
from django.contrib import admin
from .models import Project, Skill

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    list_per_page = 10

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    list_per_page = 10