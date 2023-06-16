import json
import os
import mimetypes

from django.http import HttpResponse, JsonResponse
import pandas as pd

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalDeleteView, BSModalUpdateView
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView

from .forms import FileForm, LoginUserForm, ParameterForm, ProjectForm, RegisterUserForm
from .models import Parameter, File, Project
from loader import Data
from model import Model


def load_file(request):  # надо добавить ограничение на вывод таблицы, например только первые 5 и последние 5 строк
    if request.user.is_authenticated:
        data = []
        if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            for filename, _ in request.FILES.items():
                name = request.FILES[filename].name
            df = pd.read_csv("data/files/" + name)
            columns = ['index'] + list(df.columns.values)
            count = len(columns)
            json_records = df.reset_index().to_json(orient='records')
            data = json.loads(json_records)
            context = {'d': data, 'c': columns, 'count': count}
            return render(request, 'main/table.html', context)
        else:
            form = FileForm
        return render(request, 'main/main.html', {'form': form})
    else:
        return redirect('login')


class ModelCreateView(BSModalCreateView):
    template_name = 'main/create_model.html'
    form_class = ParameterForm

    def form_valid(self, form):
        form = form.cleaned_data
        Parameter.objects.get_or_create(
            file_id=File.objects.latest('id'),
            idx=form['idx'],
            param=form['param'],
            limit=form['limit'],
            func=form['func'],
            criteria=form['criteria'],
        )
        file = File.objects.latest('id')
        parameter = Parameter.objects.latest('id')
        df = pd.read_csv("data/" + str(file.path))

        # добавить проверку на корректность ввода (есть ли столбцы в таблицы такие, как ввели)

        data = Data().preprocess(df, parameter.param)
        # string = "workers * tasks <= 40, tasks; tasks = 1, workers"

        model = Model(data, parameter.idx, parameter.param.replace(" ", ""))
        model.create(parameter.limit, parameter.func, parameter.criteria)

        df = model.model
        if not df.empty:
            df = df[df['x'] == 1]
            df = df.drop('x', axis=1)
            df.reset_index(inplace=True)
            df.to_csv('./data/download/' +
                      str(file.path).replace("files/", ""))
            columns = list(df.columns.values)
            context = {'d': df, 'c': columns}
            return render(self.request, 'main/results.html', context)
        else:
            pass
        return render(self.request, 'main/results.html', context)


def download_file(request):
    file = File.objects.latest('id').path
    name = str(file.path).replace(
        'C:\\Users\\semiz\\Desktop\\site\\low_code\\data\\files\\', "")
    filepath = './data/download/' + name
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    return response


class ProjectCreateView(BSModalCreateView):
    template_name = 'main/create_project.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form = form.cleaned_data
        Project.objects.get_or_create(
            user=self.request.user,      
            name=form['name'],
            desc=form['desc'],
        )
        return redirect('files')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('files')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('files')


def logout_user(request):
    logout(request)
    return redirect('login')


class Index(generic.ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'main/read_projects.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

class ProjectDeleteView(BSModalDeleteView):
    model = Project
    template_name = 'main/delete.html'
    success_message = 'Success'
    success_url = reverse_lazy('files')

def projects(request):
    data = {}
    if request.method == 'GET':
        projects = Project.objects.filter(user=request.user)
        data['table'] = render_to_string(
            'projects_table.html',
            {'projects': projects},
            request=request
        )
        return JsonResponse(data)