from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^summaries', views.detail, name='detail'),
]