from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("A place to catalog library books")