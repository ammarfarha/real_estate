from django.shortcuts import render, HttpResponse
from .models import Project


def home(request):
    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects})




# crispy forms
