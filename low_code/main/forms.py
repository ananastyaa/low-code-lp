import magic
import pandas as pd

from django import forms
from .models import File, Parameter, Project
from django.forms import FileInput, TextInput, Select, ValidationError
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


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
        
    def clean_file(self):
        file = self.cleaned_data.get("file", False)
        filetype = magic.from_buffer(file.read())
        if not "CSV" in filetype:
            raise ValidationError("Недопустимое расширение. Только csv и xlsx")
        if not "XLSX" in filetype:
            raise ValidationError("Недопустимое расширение. Только csv и xlsx")
        return file


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
                raise forms.ValidationError(
                    f'Похоже колонки {el} не существует в загруженной таблице')
        return data

    def clean_param(self):
        data = self.cleaned_data['param']
        d = data.replace(" ", "")
        file = File.objects.latest('id')
        df = pd.read_csv("data/" + str(file.path))
        if d not in df.columns.values:
            raise forms.ValidationError(
                f'Похоже колонки {d} не существует в загруженной таблице')
        return data


class ProjectForm(BSModalModelForm):

    class Meta:
        model = Project
        fields = ['name', 'desc']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название проекта'
            }),
            "desc": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание проекта'
            }),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
