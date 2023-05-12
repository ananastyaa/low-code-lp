from django import forms
from .models import Data
from django.forms import FileInput

class DataForm(forms.ModelForm):

   class Meta:
      model = Data
      fields = ['name_param','name_idx','file']

      widgets = {
         "file": FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Загрузите вашу таблицу'
         })
      }