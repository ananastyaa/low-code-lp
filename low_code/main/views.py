import json
import os
import mimetypes

from django.http import HttpResponse
import pandas as pd

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView

from .forms import FileForm, ParameterForm
from .models import Parameter, File
from loader import Data
from model import Model


def load_file(request): #надо добавить ограничение на вывод таблицы, например только первые 5 и последние 5 строк
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
        json_records = df.reset_index().to_json(orient ='records')
        data = json.loads(json_records)
        context = {'d': data, 'c': columns, 'count': count}
        return render(request, 'main/table.html', context)
    else:
        form = FileForm
    return render(request, 'main/main.html', {'form':form})


class ModelCreateView(BSModalCreateView):
    template_name = 'main/create_model.html'
    form_class = ParameterForm

    def form_valid(self, form):
        form = form.cleaned_data
        Parameter.objects.get_or_create(
            file_id = File.objects.latest('id'),
            idx = form['idx'],
            param = form['param'],
            limit = form['limit'],
            func = form['func'],
            criteria = form['criteria'],
            )
        file = File.objects.latest('id')
        parameter = Parameter.objects.latest('id')
        df = pd.read_csv("data/" + str(file.path))

        # добавить проверку на корректность ввода (есть ли столбцы в таблицы такие, как ввели)

        data = Data().preprocess(df, parameter.param)
        #string = "workers * tasks <= 40, tasks; tasks = 1, workers"
        
        model = Model(data, parameter.idx, parameter.param.replace(" ", ""))
        model.create(parameter.limit, parameter.func, parameter.criteria)
        
        df = model.model
        if not df.empty:
            df = df[df['x'] == 1]
            df = df.drop('x', axis=1)
            df.reset_index(inplace=True)
            df.to_csv('./data/download/' + str(file.path).replace("files/", ""))
            columns = list(df.columns.values)
            context = {'d': df, 'c': columns}
            return render(self.request, 'main/results.html', context)
        else:
            pass
        return render(self.request, 'main/results.html', context)


def download_file(request):
    file = File.objects.latest('id').path
    name = str(file.path).replace('C:\\Users\\semiz\\Desktop\\site\\low_code\\data\\files\\', "")
    filepath = './data/download/' + name
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    return response 
