from django.urls import path

from main.views import create_project, delete_project, get_education_json, get_project_json, show_education, show_main, show_experience, create_education, delete_education, show_projects, update_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/create/", create_project, name="create_project"),
    path("projects/<int:project_id>/edit/", update_project, name="update_project"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/json/", get_project_json, name="get_project_json"),
]