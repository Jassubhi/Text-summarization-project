from django import forms
from text.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'date', 'file']
