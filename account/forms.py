from django import forms

from account.models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'thumbnail', 'publishedDate']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control mb-4', 'placeholder': "Title", 'aria-describedby': "basic-addon1"}),
            'author': forms.TextInput(
                attrs={'class': 'form-control mb-4', 'placeholder': "Author", 'aria-describedby': "basic-addon2"}),
            'thumbnail': forms.TextInput(
                attrs={'class': 'form-control mb-4', 'aria-describedby': "basic-addon3"}),
            'publishedDate': forms.TextInput(
                attrs={'class': 'form-control mb-4', 'aria-describedby': "basic-addon3"}),
        }


class BookListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = None
    class Meta:
        model = UserBookList
        fields = ['review', 'favorites', 'status']
        widgets = {
            'review': forms.Textarea(
                attrs={'class': 'form-control'}),
            'favorites': forms.CheckboxInput(
                attrs={'class': 'form-check-input g-2 mb-4 fs-5'}),
            'status': forms.Select(
                attrs={'class': 'form-select form-select-lg mb-4'}),
        }
