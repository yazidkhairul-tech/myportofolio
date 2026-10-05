from django.urls import path

from main.views import (create_education_ajax, create_project, create_project_ajax, delete_project, get_education_json, get_project_json,
    login_user, logout_user, register, show_education, show_main, show_experience,
    create_education, delete_education, show_projects, toggle_star, toggle_star_education, update_project)

app_name = "main"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/add-ajax/", create_education_ajax, name="create_education_ajax"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("education/<uuid:education_id>/star/", toggle_star_education, name="toggle_star_education"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<int:project_id>/edit/", update_project, name="update_project"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/json/", get_project_json, name="get_project_json"),
    path("projects/<int:project_id>/star/", toggle_star, name="toggle_star"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]
