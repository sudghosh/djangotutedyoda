from django import forms
from .models import Csvs

class upload_form(forms.ModelForm):
   
    class Meta:
        model = Csvs
        fields =('file_name',)