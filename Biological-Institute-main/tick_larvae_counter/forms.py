from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']  # Inclua outros campos conforme necessário

class ManualCountForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['manual_count']  # Inclui apenas o campo para contagem manual.
