from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name="files"),
    path('create_model', views.ModelCreateView.as_view(), name='create_model')
]