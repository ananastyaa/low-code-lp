import pandas as pd

from django import forms
from .models import File, Parameter
from django.forms import FileInput, TextInput, Select
from bootstrap_modal_forms.forms import BSModalModelForm

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


class ParameterForm(BSModalModelForm):

   class Meta:
      model = Parameter
      fields = ['idx', 'param', 'limit', 'func', 'criteria']

      widgets = {
         "idx": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите индексы'
         }),
         "param": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите параметры'
         }),
         "limit": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ограничения (a * b < 8, где a, b - параметры)'
         }),
         "func": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите целевую функцию'
         }),
         "criteria": Select(attrs={
            'class': 'form-control',
         }),
   }

   def clean_idx(self):
      data = self.cleaned_data['idx']
      d = data.replace(" ", "").split(',')
      file = File.objects.latest('id')
      df = pd.read_csv("data/" + str(file.path))
      for el in d:
         if el not in df.columns.values:
            raise forms.ValidationError(f'Похоже колонки {el} не существует в загруженной таблице')
      return data 
   
   def clean_param(self):
      data = self.cleaned_data['param']
      d = data.replace(" ", "")
      file = File.objects.latest('id')
      df = pd.read_csv("data/" + str(file.path))
      if d not in df.columns.values:
         raise forms.ValidationError(f'Похоже колонки {d} не существует в загруженной таблице')
      return data 
