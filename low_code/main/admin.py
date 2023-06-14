from django.contrib import admin

# Register your models here.

from .models import File, Parameter, Project
# Зарегистрируйте вашу модель здесь.
admin.site.register(File)
admin.site.register(Parameter)
admin.site.register(Project)