from django.shortcuts import render, HttpResponse
from .models import Project
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext


def home(request):
    projects = Project.objects.all()
    trans = translate(language='ar')
    context = {
        'sample_text': _("Hello"),
        'trans': trans,
        'projects': projects,
    }
    return render(request, 'home.html', context)


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text
