from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_todo, name='add'),
    path('toggle/<int:pk>/', views.toggle, name='toggle'),
    path('edit/<int:pk>/', views.edit_todo, name='edit'),
    path('delete/<int:pk>/', views.delete_todo, name='delete'),
]
