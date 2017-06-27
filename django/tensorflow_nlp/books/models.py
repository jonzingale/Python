from django.db import models

# b = Book(title=str, author='S. Mac Lane',lccn='QA169 .M33 1994', isbn='0387900357', pub_year = '1994')

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    lccn = models.CharField(max_length=200)
    isbn = models.BigIntegerField(default=0)
    pub_year = models.IntegerField(default=0)

    def __str__(self):
      return self.title
