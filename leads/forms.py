from django import forms
from django.forms import ModelForm
from .models import Lead


class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    project_name = forms.CharField(max_length=50)

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'project_name',
        )