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


from datetime import date

@login_required
def habit_list(request):
    today = date.today()

    # Filter habits based on the start and end date
    habits_to_do_today = Habit.objects.filter(
        user=request.user,
        start_date__lte=today,  # Habit's start date is less than or equal to today
        end_date__gte=today,    # Habit's end date is greater than or equal to today
        completed=False
    )

    # Get the IDs of the habits marked as done today
    done_checkoffs = CheckOff.objects.filter(habit__in=habits_to_do_today, timestamp__date=today)
    done_habits = [checkoff.habit.id for checkoff in done_checkoffs]

    return render(request, 'habit_tracker/habit_list.html', {'habits': habits_to_do_today, 'done_habits': done_habits})




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


from datetime import date  

@login_required
def show_current_habits(request):
    today = date.today()
    current_habits = Habit.objects.filter(
        user=request.user,
        start_date__lte=today,  # Habit's start date is less than or equal to today
        end_date__gte=today,    # Habit's end date is greater than or equal to today
        completed=False
    )
    return render(request, 'habit_tracker/current_habits.html', {'current_habits': current_habits})



from datetime import date  # Don't forget to import date

@login_required
def show_completed_habits(request):
    today = date.today()
    completed_habits_done = Habit.objects.filter(
        user=request.user,
        completed=True,
    )
    completed_habits_time_ended = Habit.objects.filter(
        user=request.user,
        end_date__lt=today,
        completed=False
    )
    return render(request, 'habit_tracker/completed_habits.html', {
        'completed_habits_done': completed_habits_done,
        'completed_habits_time_ended': completed_habits_time_ended
    })





from django.utils import timezone

@login_required
def toggle_habit_done(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    
    # Check if habit is already done today
    today = timezone.now().date()
    checkoff = CheckOff.objects.filter(habit=habit, timestamp__date=today).first()

    if checkoff:
        checkoff.delete()
    else:
        CheckOff.objects.create(habit=habit)
    
    return redirect('habit_list')



