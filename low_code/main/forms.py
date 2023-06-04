from django import forms
from .models import File, Parameter
from django.forms import FileInput, TextInput
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
      fields = ['idx', 'param', 'limit']

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
            'placeholder': 'Введите ограничения формулой вида (a < 8)'
         }),
      }
