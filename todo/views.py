from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm


def index(request):
	todos = Todo.objects.all()
	return render(request, 'todo/home.html', {'todos': todos})


def add_todo(request):
	if request.method == 'POST':
		form = TodoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('todo:index')
	else:
		form = TodoForm()
	return render(request, 'todo/form.html', {'form': form, 'title': 'Add Todo'})


def edit_todo(request, pk):
	todo = get_object_or_404(Todo, pk=pk)
	if request.method == 'POST':
		form = TodoForm(request.POST, instance=todo)
		if form.is_valid():
			form.save()
			return redirect('todo:index')
	else:
		form = TodoForm(instance=todo)
	return render(request, 'todo/form.html', {'form': form, 'title': 'Edit Todo'})


def delete_todo(request, pk):
	todo = get_object_or_404(Todo, pk=pk)
	if request.method == 'POST':
		todo.delete()
		return redirect('todo:index')
	return render(request, 'todo/confirm_delete.html', {'todo': todo})


def toggle(request, pk):
	todo = get_object_or_404(Todo, pk=pk)
	todo.completed = not todo.completed
	todo.save()
	return redirect('todo:index')
