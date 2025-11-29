from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['file', 'description']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '*/*'}),
            'description': forms.TextInput(attrs={'placeholder': 'Short description (e.g., Chest X-Ray)'}),
        }
