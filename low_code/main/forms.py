from django import forms
from .models import Data
from django.forms import FileInput, TextInput

class DataForm(forms.ModelForm):

   class Meta:
      model = Data
      fields = ['name_param','name_idx','file']

      widgets = {
         "file": FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Загрузите вашу таблицу'
         }),
         "name_param": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название столбца с параметрами'
         }),
         "name_idx": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название столбцов индексов'
         }),
      }