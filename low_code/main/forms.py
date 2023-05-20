from django import forms
from .models import File, Parameter
from django.forms import FileInput, TextInput

class FileForm(forms.ModelForm):

   class Meta:
      model = File
      fields = ['path', 'name', 'extension']

      widgets = {
         "path": FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Загрузите вашу таблицу'
         }),
      }