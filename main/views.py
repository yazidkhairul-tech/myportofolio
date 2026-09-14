from django.shortcuts import render
 
from main.models import Experience, Education
 
 
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
    context = {
        "name": "Yazid Khairul Firmansyah",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)