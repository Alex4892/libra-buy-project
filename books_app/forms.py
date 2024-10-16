from django import forms

from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("name", "author", "genre", "description", "publication", "publication_year", "price")