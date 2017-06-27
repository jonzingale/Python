from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    lccn = models.CharField(max_length=200)
    isbn = models.BigIntegerField(default=0)
    pub_year = models.IntegerField(default=0)

    def __str__(self):
      return self.title