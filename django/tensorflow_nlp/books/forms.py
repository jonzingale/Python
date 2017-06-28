from django.forms import modelformset_factory
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
  class Meta:
      model = Book
      fields = ('title',)
      widgets = {'title': forms.Textarea(attrs={'cols': 40, 'rows': 1})}