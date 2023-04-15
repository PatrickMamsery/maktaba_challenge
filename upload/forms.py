from django import forms
from .models import CSVFile

class CSVFileUploadForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ('file_name', 'file', 'active')
        widgets = {
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'custom2-file-input'}),
            'active': forms.CheckboxInput(attrs={'class': ''})
        }