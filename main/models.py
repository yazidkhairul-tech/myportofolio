import uuid
from django.contrib.auth.models import User
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
 
    def __str__(self):
        return self.title
 
    @property
    def is_ongoing(self):
        return self.ended_at is None
 
 
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    score = models.FloatField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    starred_by = models.ManyToManyField(User, related_name="starred_education", blank=True)
 
    class Meta:
        ordering = ['-started_at']
 
    def __str__(self):
        return f"{self.program} - {self.institution_name}"
 
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(
        max_length=255,
        blank=True,
        help_text="Pisahkan setiap teknologi dengan koma, contoh: Django, PostgreSQL, React",
    )
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True)
    project_url = models.URLField(blank=True, help_text="Link demo/live project (opsional)")
    source_url = models.URLField(blank=True, help_text="Link repository/source code (opsional)")
    started_at = models.DateField()
    is_ongoing = models.BooleanField(default=False)
    ended_at = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    starred_by = models.ManyToManyField(User, related_name="starred_projects", blank=True)
 
    class Meta:
        ordering = ["-is_featured", "-started_at"]
 
    def __str__(self):
        return self.title
 
    def tech_list(self):
        """Dipakai di template: {% for tech in project.tech_list %}"""
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]
