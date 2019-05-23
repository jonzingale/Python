from django.db import models

from django.contrib.sites.models import Site
from django.contrib.sitemaps import Sitemap

class CurriculumVitae(models.Model):
  project = models.CharField(max_length=200)
  location = models.CharField(max_length=200)
  start_date = models.CharField(max_length=200)
  end_date = models.BigIntegerField(default=0)
  tags = models.IntegerField(default=0)

  def __str__(self):
    return self.project