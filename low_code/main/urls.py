from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_file, name="files"),
    path('create_model', views.ModelCreateView.as_view(), name='create_model'),
    path('download', views.download_file, name='download'),
    path('create_project', views.ProjectCreateView.as_view(), name='create_project'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),

]