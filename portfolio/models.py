from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    def __str__(self):
        return self.title

CATEGORY_CHOICES = [
    ('Programming', 'Programming'),
    ('Cloud', 'Cloud'),
    ('DevOps', 'DevOps'),
    ('others', 'others')
]

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.name} ({self.category})'
