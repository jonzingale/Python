from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^summaries', views.detail, name='detail'),
    # url(r'^js/d3\.v4\.min\.js', views.d3, name='d3'),
    # url(r'^nunitoSans\.css', views.nunitoSans, name='nunitoSans'),
    # url(r'^js/prismacolorsummary\.css', views.style, name='style')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)