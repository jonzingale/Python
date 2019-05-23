from django.db import models

from django.contrib.sites.models import Site
from django.contrib.sitemaps import Sitemap

class CurriculumVitae(models.Model):
  project = models.CharField(max_length=200)
  location = models.CharField(null=True, blank=True, max_length=200)
  start_date = models.CharField(null=True, blank=True, max_length=200)
  end_date = models.CharField(null=True, default='Present', max_length=200)
  tags = models.CharField(null=True, blank=True, max_length=200)
  description = models.CharField(max_length=3000, null=True, blank=True)

  def __str__(self):
    return self.project

class Publications(models.Model):
  title = models.CharField(max_length=200)
  journal = models.CharField(null=True, blank=True, max_length=200)
  url = models.CharField(null=True, blank=True, max_length=200)
  pub_date = models.CharField(null=True, default='Present', max_length=200)
  tags = models.CharField(null=True, blank=True, max_length=200)
  description = models.CharField(max_length=3000, null=True, blank=True)

  def __str__(self):
    return self.title