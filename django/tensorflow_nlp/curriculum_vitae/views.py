from django.shortcuts import render
from django.http import HttpResponse
from .forms import CurriculumVitaeForm
from django.shortcuts import redirect

import django_rq
# from loc_book_scraper import find_book

def index(request):
    return HttpResponse("Towards an automated curriculum vitae.")

def detail(request, project_id):
    return HttpResponse("You're looking at project %s." % project_id)

def projects_new(request):
    if request.method == "POST":
        form = CurriculumVitaeForm(request.POST)
        title = request.POST['title']

        if form.is_valid():
            # be sure that redis is running: start_redis
            # to pick up queue run: python manage.py rqworker default
            queue = django_rq.get_queue('default')
            queue.enqueue(find_book, title)
    else:
        form = CurriculumVitaeForm()
    return render(request, 'projects/project_edit.html', {'form': form})