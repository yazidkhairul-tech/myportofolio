from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from portofolio.forms import EducationForm
from main.models import Experience, Education
from django.db.models import Q

 
def show_main(request):
    context = {
        "name": "Yazid",
        "npm": "2506537064",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "An undergraduate student of Computer Science in Indonesia with a strong enthusiasm for IT and its management. I consider myself a confident and optimistic individual. Looking up for new knowledges and experiences further."
        ),
        "education_list": Education.objects.all(),
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
