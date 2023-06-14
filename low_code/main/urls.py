from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_file, name="files"),
    path('create_model', views.ModelCreateView.as_view(), name='create_model'),
    path('download', views.download_file, name='download'),
    path('create_project', views.ProjectCreateView.as_view(), name='create_project'),
]