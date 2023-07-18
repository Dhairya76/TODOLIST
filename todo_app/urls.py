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
    path('search-todo-category/', views.search_todo_category,
         name='search_todo_category'),
    path('add-subtask/', views.add_subtask, name='add_subtask'),
    path('search-subtask/', views.search_subtask, name='search_subtask'),
    path('delete-subtask/<int:subtask_id>/', views.delete_subtask, name='delete_subtask'),
    path('change-status-subtask/<int:subtask_id>/<str:subtask_status>',
         views.change_status_subtask, name='change_status_subtask'),

]
