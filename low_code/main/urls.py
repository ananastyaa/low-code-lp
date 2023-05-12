from django.urls import path
from . import views
from .views import start
urlpatterns = [
    path('', views.start, name="files")

]