from django import forms


class MeaniningForm(forms.Form):
    word = forms.CharField()