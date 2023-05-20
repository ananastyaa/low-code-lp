import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FileForm
import pandas as pd
from .models import File
from loader import Client


def start(request): #надо добавить ограничение на вывод таблицы, например только первые 5 и последние 5 строк
    data = []
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        for filename, file in request.FILES.items():
            name = request.FILES[filename].name
        df = pd.read_csv("data/files/" + name)
        columns = ['index'] + list(df.columns.values)
        count = len(columns)
        # parsing the DataFrame in json format.
        json_records = df.reset_index().to_json(orient ='records')
        data = json.loads(json_records)
        client = Client()
        res = client.response(df)
        context = {'d': data, 'c': columns, 'count': count, 'res': res}
        return render(request, 'main/main.html', context)
    else:
        form = FileForm
    return render(request, 'main/main.html', {'form':form})