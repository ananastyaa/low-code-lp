from django.contrib import admin

# Register your models here.

from .models import File, Parameter
# Зарегистрируйте вашу модель здесь.
admin.site.register(File)
admin.site.register(Parameter)