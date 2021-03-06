from django.shortcuts import render
from django.http import HttpResponse
from .models import Summary

def detail(request):
    json = Summary.objects.first().json
    title = Summary.objects.first().image_title
    # html = """
    # <html><body>
    #   <div class='title'>{0}</div>
    #   <div class='spacer'></div>
    #   <div class='json'>{1}</div>
    # </body></html>
    # """.format(title, json)
    # return HttpResponse(html)
    return render(request, 'prisma_summaries/prisma.html') #, {'title': title, 'cal': cal})

# def d3(request):
#   return render(request, 'prisma_summaries/js/d3.v4.min.js')

# def nunitoSans(request):
#   return render(request, 'prisma_summaries/fonts/nunitoSans.css')

# def style(request):
#   return render(request, 'prisma_summaries/js/prismacolorsummary.css')