from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from todo_app.forms import TODOForm
from todo_app.models import TODO
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        username = user.username
        print(username)

        # return render(request, 'index.html', context={'form': form, 'todos': todos})
        paginator = Paginator(todos, 3)  # Display 5 todos per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', context={'form': form, 'page_obj': page_obj , 'username': username})


@login_required(login_url='login')
def search_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        search_query = request.GET.get('search')

        if search_query:
            todos = TODO.objects.filter(
                user=user, title__icontains=search_query).order_by('priority')
        else:
            todos = TODO.objects.filter(user=user).order_by('priority')

        paginator = Paginator(todos, 3)  # Display 3 todos per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', context={'form': form, 'page_obj': page_obj})


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
                messages.success(request, "Your account has been created. Please log in.")
                return redirect('login')
        else:
            messages.error(request, "There was an error creating your account.")
            return render(request, 'register.html', context=context)


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
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
    # messages.info(request, "Do you want to delete this task?")
    # TODO.objects.get(pk=id).delete()
    # return redirect('home')
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
