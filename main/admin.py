from django.contrib import admin

from main.models import Experience, Education


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "started_at", "ended_at")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("program", "institution_name", "started_at", "ended_at")
    search_fields = ("program", "institution_name", "description")