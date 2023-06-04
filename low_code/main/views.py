import json
import pandas as pd

from django.shortcuts import render
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView

from .forms import FileForm, ParameterForm
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
        json_records = df.reset_index().to_json(orient ='records')
        data = json.loads(json_records)
        client = Client()
        res = client.response(df)
        context = {'d': data, 'c': columns, 'count': count, 'res': res}
        return render(request, 'main/table.html', context)
    else:
        form = FileForm
    return render(request, 'main/main.html', {'form':form})


class ModelCreateView(BSModalCreateView):
    template_name = 'main/create_model.html'
    form_class = ParameterForm
    success_message = 'Success'
    success_url = reverse_lazy('')