from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Habit
from .forms import HabitForm  # Import HabitForm here

@login_required
def create_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return HttpResponseRedirect('/habits')
    else:
        form = HabitForm()

    return render(request, 'habit_tracker/create_habit.html', {'form': form})


from django.shortcuts import render
from .models import Habit

def habit_list(request):
    habits = Habit.objects.all()
    return render(request, 'habit_tracker/habit_list.html', {'habits': habits})



