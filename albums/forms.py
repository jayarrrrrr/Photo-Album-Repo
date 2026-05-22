from django import forms
from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Album title'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 5, 'placeholder': 'Album description'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
            'caption': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Photo caption'}),
        }
