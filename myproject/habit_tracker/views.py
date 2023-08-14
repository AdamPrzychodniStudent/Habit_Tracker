from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit
from .forms import HabitForm  

from .models import Habit, CheckOff
from .forms import HabitForm


def welcome(request):
    return render(request, 'habit_tracker/welcome.html')


@login_required
def habit_list(request):
    habits = Habit.objects.all()
    return render(request, 'habit_tracker/habit_list.html', {'habits': habits})


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


@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    
    if request.method == 'POST':
        if 'check_off' in request.POST:
            habit.completed = True  # Set the habit's completed field to True
            habit.save()
            messages.success(request, "Habit marked as completed!")
            return redirect('habit_list')
        elif 'delete_habit' in request.POST:
            habit.delete()
            messages.success(request, "Habit deleted successfully!")
            return redirect('habit_list')
            
    return render(request, 'habit_tracker/edit_habit.html', {'habit': habit})


