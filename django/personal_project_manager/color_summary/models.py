from django.db import models

from django.contrib.sites.models import Site
from django.contrib.sitemaps import Sitemap

class Summary(models.Model):
  image_title = models.CharField(max_length=200)
  json = models.CharField(null=True, blank=True, max_length=200)
  image = models.CharField(default="someURL", max_length=100)

  def __str__(self):
    return self.title