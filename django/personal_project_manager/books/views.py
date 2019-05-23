from django.shortcuts import render
from django.http import HttpResponse
from .forms import BookForm
from django.shortcuts import redirect

import django_rq
from loc_book_scraper import find_book

def index(request):
    return HttpResponse("A place to catalog library books")

def detail(request, book_id):
    return HttpResponse("You're looking at book %s." % book_id)

def books_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        title = request.POST['title']

        if form.is_valid():
            # be sure that redis is running: start_redis
            # to pick up queue run: python manage.py rqworker default
            queue = django_rq.get_queue('default')
            queue.enqueue(find_book, title)
            # return redirect('book_detail', pk=post.pk) # HOW TO REDIRECT?
    else:
        form = BookForm()
    return render(request, 'books/book_edit.html', {'form': form})