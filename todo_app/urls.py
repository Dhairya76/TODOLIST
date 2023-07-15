from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # path('', views.taskList,name='tasks'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('add-todo/', views.add_todo, name='add_todo'),
    path('logout/', views.logout, name='logout'),
    path('delete-todo/<int:id>', views.delete_todo, name='delete_todo'),
    path('change-status/<int:id>/<str:status>',
         views.change_status, name='change_status'),
    path('search-todo/', views.search_todo, name='search_todo'),

]
