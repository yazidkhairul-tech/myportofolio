import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from portofolio.forms import EducationForm, ProjectForm
from main.models import Experience, Education, Project
from django.db.models import Count, Exists, OuterRef, Q


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

 
def show_main(request):
    context = {
        "name": "Yazid",
        "npm": "2506537064",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "An undergraduate student of Computer Science in Indonesia with a strong enthusiasm for IT and its management. I consider myself a confident and optimistic individual. Looking up for new knowledges and experiences further."
        ),
        "education_list": Education.objects.all(),
        "last_login": request.COOKIES.get(
            "last_login", "Belum ada sesi login / Cookie tidak ditemukan"
        ),
    }
    return render(request, "index.html", context)
 
 
def show_experience(request):
    context = {
        "name": "Yazid Khairul Firmansyah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
 
 
def show_education(request):
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education = [item.object for item in education]
    query = request.GET.get("institution_name", "").strip()

    context = {
        "name": "Yazid Khairul Firmansyah",
        "education_list": education,
        "query": query,
    }
    return render(request, "education.html", context)

def get_education_json(request):
      query = request.GET.get("q", "").strip()
      education = Education.objects.all()

      if query:
          education = education.filter(
              Q(institution_name__icontains=query) | Q(program__icontains=query)
          )

      education_json = serializers.serialize("json", education)
      return HttpResponse(education_json, content_type="application/json")

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Yazid",
        "form": form,
    }

    return render(request, "education_form.html", context)

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def show_projects(request):
    query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
 
    if query:
        projects = projects.filter(title__icontains=query)
 
    context = {
        "name": "Yazid",
        "project_list": projects,
        "query": query,
        "is_editor": is_editor(request.user),
    }
    return render(request, "projects.html", context)
 
 
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None, request.FILES or None)
 
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil ditambahkan!")
        return redirect("main:show_projects")
 
    context = {
        "name": "Yazid",
        "form": form,
    }
    return render(request, "project_form.html", context)
 
 
@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
 
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")
 
    context = {
        "name": "Yazid",
        "form": form,
        "project": project,
    }
    return render(request, "project_form.html", context)
 
 
@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
 
    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyek berhasil dihapus!")
        return redirect("main:show_projects")
 
    return redirect("main:show_projects")
 
 
def get_project_json(request):
    query = request.GET.get("q", "").strip()
    projects = Project.objects.all()
 
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(tech_stack__icontains=query)
        )
 
    through_model = Project.starred_by.through
    projects = projects.annotate(star_count=Count("starred_by", distinct=True))
    if request.user.is_authenticated:
        projects = projects.annotate(
            is_starred=Exists(
                through_model.objects.filter(
                    project_id=OuterRef("pk"), user_id=request.user.pk
                )
            )
        )

    data = [
        {
            "pk": project.pk,
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "thumbnail": project.thumbnail.name if project.thumbnail else "",
                "project_url": project.project_url,
                "source_url": project.source_url,
                "started_at": project.started_at.isoformat(),
                "ended_at": project.ended_at.isoformat() if project.ended_at else None,
                "is_ongoing": project.is_ongoing,
                "is_featured": project.is_featured,
                "star_count": project.star_count,
                "is_starred": getattr(project, "is_starred", False),
            },
        }
        for project in projects
    ]
    return JsonResponse(data, safe=False)


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    return render(request, "register.html", {"name": "Yazid", "form": form})


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response
    return render(request, "login.html", {"name": "Yazid", "form": form})


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login/")
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return redirect("main:show_projects")
