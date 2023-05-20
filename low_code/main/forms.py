from django import forms
from .models import File, Parameter
from django.forms import FileInput, TextInput

class FileForm(forms.ModelForm):

   class Meta:
      model = File
      fields = ['path']

      widgets = {
         "path": FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Загрузите вашу таблицу'
         }),
      }

"""
class ParameterForm(forms.ModelForm):

   class Meta:
      model = Parameter
      fields = ['col_idx', 'col_param']

      widgets = {
         "col": FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Загрузите вашу таблицу'
         }),
      }
"""