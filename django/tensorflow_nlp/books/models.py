from django.db import models

from django.contrib.sites.models import Site
from django.contrib.sitemaps import Sitemap

class BookSiteMap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.pub_year

    def location(self, item):
      return("/"+item.title)


class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=200)
  lccn = models.CharField(max_length=200)
  isbn = models.BigIntegerField(default=0)
  pub_year = models.IntegerField(default=0)

  def __str__(self):
    return self.title