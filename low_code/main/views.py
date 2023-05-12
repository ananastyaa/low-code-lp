import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import DataForm
import pandas as pd
from .models import Data


def start(request): #надо добавить ограничение на вывод таблицы, например только первые 5 и последние 5 строк
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        for filename, file in request.FILES.items():
            name = request.FILES[filename].name
        df = pd.read_csv("data/files/" + name)
        columns = ['index'] + list(df.columns.values)
        count = len(columns)
        # parsing the DataFrame in json format.
        json_records = df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'d': data, 'c': columns, 'count': count}
        return render(request, 'main/main.html', context)
    else:
        form = DataForm
    return render(request, 'main/main.html', {'form':form})