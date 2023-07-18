from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from todo_app.forms import TODOForm, SubTaskForm
from todo_app.models import TODO, SubTask
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        username = user.username
        paginator = Paginator(todos, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', context={'form': form, 'page_obj': page_obj, 'username': username})


@login_required(login_url='login')
def search_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        username = user.username
        search_query = request.GET.get('search')

        if search_query:
            todos = TODO.objects.filter(
                user=user, title__icontains=search_query).order_by('priority')
        else:
            todos = TODO.objects.filter(user=user).order_by('priority')

        print(todos)

        paginator = Paginator(todos, 3)  # Display 3 todos per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', context={'form': form, 'page_obj': page_obj, 'username': username})


@login_required(login_url='login')
def search_todo_category(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        username = user.username
        search_query_category = request.GET.get('search')

        if search_query_category:
            todos = TODO.objects.filter(
                user=user, category__icontains=search_query_category).order_by('priority')
        else:
            todos = TODO.objects.filter(user=user).order_by('priority')

        paginator = Paginator(todos, 3)  # Display 3 todos per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', context={'form': form, 'page_obj': page_obj, 'username': username})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
        return render(request, 'login.html', context=context)


def register(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form,
        }
        return render(request, 'register.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form,
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                messages.success(
                    request, "Your account has been created. Please log in.")
                return redirect('login')
        else:
            messages.error(
                request, "There was an error creating your account.")
            return render(request, 'register.html', context=context)


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form})


def logout(request):
    logoutUser(request)
    return redirect('login')


def delete_todo(request, id):
    todo = TODO.objects.get(pk=id)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('home')

    context = {
        'todo': todo,
    }
    return render(request, 'delete_todo.html', context=context)


def change_status(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')


@login_required(login_url='login')
def add_subtask(request):
    if request.user.is_authenticated:
        user = request.user
        form = SubTaskForm()
        username = user.username
        if request.method == 'POST':
            form = SubTaskForm(request.POST)
            if form.is_valid():
                subtask = form.save(commit=False)
                subtask.user = user
                subtask.save()
                return redirect("search_subtask")

        context = {
            'form': form,
            'username': username,
        }

        return render(request, 'subtask.html', context=context)


@login_required(login_url='login')
def search_subtask(request):
    if request.user.is_authenticated:
        user = request.user
        form = SubTaskForm()
        username = user.username
        subtasks = SubTask.objects.only(
            'subtask_title', 'subtask_status', 'subtask_priority').all().order_by('subtask_priority')
        print(subtasks)
        

        paginator = Paginator(subtasks, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        subtask_values = [(subtask.subtask_title, subtask.subtask_status,
                           subtask.subtask_priority) for subtask in page_obj]
        print(subtask_values)

        context = {
            'form': form,
            'subtasks': page_obj,
            'username': username,
            'page_obj': page_obj,
        }

        return render(request, 'subtask.html', context=context)


def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == 'POST':
        subtask.delete()
        return redirect('search_subtask')

    context = {
        'subtask': subtask
    }
    return render(request, 'delete_subtask.html', context=context)


def change_status_subtask(request, subtask_id, subtask_status):
    subtask = SubTask.objects.get(id=subtask_id)
    subtask.subtask_status = subtask_status
    subtask.save()
    print(subtask.subtask_status)
    return redirect('search_subtask')
