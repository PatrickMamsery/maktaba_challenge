from django import forms
from .models import CSVFile

class CSVFileUploadForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ('file_name', 'file', 'active')