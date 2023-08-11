from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from .models import Habit
from .forms import HabitForm  
from django.contrib import messages

@login_required
def create_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Habit successfully added!')  # Add this line
            return HttpResponseRedirect('/habit_tracker/')  # Redirect to habit_list
    else:
        form = HabitForm()

    return render(request, 'habit_tracker/create_habit.html', {'form': form})


def habit_list(request):
    habits = Habit.objects.all()
    return render(request, 'habit_tracker/habit_list.html', {'habits': habits})


def welcome(request):
    return render(request, 'habit_tracker/welcome.html')




