from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Habit, CheckOff
from .forms import HabitForm

from datetime import date, timedelta, datetime
from django.utils import timezone

from .utils import create_example_habits


# Welcome view
def welcome(request):
    """
    Renders the welcome page.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    return render(request, 'habit_tracker/welcome.html')


# Display a list of habits
@login_required
def habit_list(request):
    """
    Lists habits that need to be done today for the logged-in user.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    create_example_habits(request.user)
    today = date.today()

    # Filter habits based on the start and end date
    habits_to_do_today = Habit.objects.filter(
        user=request.user,
        start_date__lte=today,  
        end_date__gte=today,    
        completed=False
    )

    # Get the IDs of the habits marked as done today
    done_checkoffs = CheckOff.objects.filter(habit__in=habits_to_do_today, timestamp__date=today)
    done_habits = [checkoff.habit.id for checkoff in done_checkoffs]

    return render(request, 'habit_tracker/habit_list.html', {'habits': habits_to_do_today, 'done_habits': done_habits})


# Create a new habit
@login_required
def create_habit(request):
    """
    Creates a new habit.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Habit successfully added!')  
            return HttpResponseRedirect('/habit_tracker/')  
    else:
        form = HabitForm()

    return render(request, 'habit_tracker/create_habit.html', {'form': form})


# Edit an existing habit
@login_required
def edit_habit(request, habit_id):
    """
    Edits an existing habit identified by habit_id.

    :param request: HttpRequest object
    :param habit_id: Integer, the id of the habit to edit
    :return: HttpResponse object containing rendered HTML
    """
    habit = get_object_or_404(Habit, id=habit_id)
    
    if request.method == 'POST':
        if 'check_off' in request.POST:
            habit.completed = True  
            habit.save()
            messages.success(request, "Habit marked as completed!")
            return redirect('habit_list')
        elif 'delete_habit' in request.POST:
            habit.delete()
            messages.success(request, "Habit deleted successfully!")
            return redirect('habit_list')
            
    return render(request, 'habit_tracker/edit_habit.html', {'habit': habit})


# Function toggles the "done" status of a specific habit for today
@login_required
def toggle_habit_done(request, habit_id):
    """
    Toggles the "done" status of a specific habit for today.

    :param request: HttpRequest object
    :param habit_id: Integer, the id of the habit to toggle
    :return: HttpResponse object redirecting to habit_list view
    """
    habit = get_object_or_404(Habit, id=habit_id)
    
    # Check if habit is already done today
    today = timezone.now().date()
    checkoff = CheckOff.objects.filter(habit=habit, timestamp__date=today).first()

    if checkoff:
        checkoff.delete()
    else:
        CheckOff.objects.create(habit=habit)
    
    return redirect('habit_list')

# Show the currently active habits
@login_required
def show_current_habits(request):
    """
    Shows the currently active habits for the logged-in user.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    today = date.today()
    current_habits = Habit.objects.filter(
        user=request.user,
        start_date__lte=today,  
        end_date__gte=today,    
        completed=False
    )
    return render(request, 'habit_tracker/current_habits.html', {'current_habits': current_habits})


# Show habits which have the same periodicty e.g. Daily 
@login_required
def show_same_periodicity_habits(request, period):
    """
    Shows habits for the logged-in user with the same periodicity.

    :param request: HttpRequest object
    :param period: String, periodicity of the habits to filter
    :return: HttpResponse object containing rendered HTML
    """
    habits = Habit.objects.filter(user=request.user, period=period)
    return render(request, 'habit_tracker/same_periodicity_habits.html', {'habits': habits, 'period': period})


# Show habits which user completed
@login_required
def show_completed_habits(request):
    """
    Shows the habits that the logged-in user has completed.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
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


# Show how long are the streak in habits
@login_required
def show_streaks(request):
    """
    Shows the length of streaks for each habit of the logged-in user.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    user_habits = Habit.objects.filter(user=request.user)
    streaks_data = []

    for habit in user_habits:
        checkoffs = CheckOff.objects.filter(habit=habit).order_by('timestamp')
        if checkoffs.exists():
            current_streak = 0
            longest_streak = 0
            temp_streak = 0
            prev_date = checkoffs.first().timestamp.date()

            for checkoff in checkoffs[1:]:
                curr_date = checkoff.timestamp.date()

                if (curr_date - prev_date).days == 1:
                    temp_streak += 1
                else:
                    temp_streak = 0

                longest_streak = max(longest_streak, temp_streak)
                prev_date = curr_date

            streaks_data.append({
                'name': habit.name, 
                'streak': longest_streak  # change this to the longest streak
            })

    sorted_streaks = sorted(streaks_data, key=lambda x: x['streak'], reverse=True)

    return render(request, 'habit_tracker/show_streaks.html', {'streaks': sorted_streaks})



# Calculate and show with what habits user has issues
@login_required
def show_struggled_habits(request):
    """
    Shows habits with which the logged-in user has issues or struggles.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    last_month_start = date.today() - timedelta(days=30)
    last_month_end = date.today()
    
    habits = Habit.objects.filter(
        user=request.user,
        start_date__lte=last_month_end,
        end_date__gte=last_month_start
    )
    
    struggled_habits_data = []
    
    for habit in habits:
        if habit.period == Habit.DAILY:
            total_days_last_month = (last_month_end - max(habit.start_date, last_month_start)).days + 1
        elif habit.period == Habit.WEEKLY:
            total_days_last_month = ((last_month_end - max(habit.start_date, last_month_start)).days // 7) + 1
        elif habit.period == Habit.MONTHLY:
            total_days_last_month = ((last_month_end - max(habit.start_date, last_month_start)).days // 30) + 1
            
        checkoffs_last_month = CheckOff.objects.filter(
            habit=habit,
            timestamp__date__gte=max(habit.start_date, last_month_start),
            timestamp__date__lte=min(habit.end_date, last_month_end)
        ).count()
        
        missed_days = total_days_last_month - checkoffs_last_month
        struggle_score = (missed_days / total_days_last_month) * 100  # percentage of missed days
        
        struggled_habits_data.append({
            'name': habit.name,
            'struggle_score': struggle_score
        })
        
    sorted_struggled_habits = sorted(struggled_habits_data, key=lambda x: x['struggle_score'], reverse=True)
    
    return render(request, 'habit_tracker/show_struggled_habits.html', {'struggled_habits': sorted_struggled_habits})


# Show how many repition are already checked off and how many left 
@login_required
def show_repetitions(request):
    """
    Shows the number of repetitions completed and remaining for each habit.

    :param request: HttpRequest object
    :return: HttpResponse object containing rendered HTML
    """
    habits = Habit.objects.filter(user=request.user)
    habit_repetitions = []
    
    for habit in habits:
        total_days = (habit.end_date - habit.start_date).days + 1
        total_reps = 0
        
        if habit.period == Habit.DAILY:
            total_reps = total_days
        elif habit.period == Habit.WEEKLY:
            total_reps = total_days // 7
        elif habit.period == Habit.MONTHLY:
            total_reps = total_days // 30  
        
        # Calculate remaining repetitions
        done_reps = CheckOff.objects.filter(habit=habit).count()
        remaining_reps = total_reps - done_reps
        
        habit_repetitions.append({
            'name': habit.name,
            'total_reps': total_reps,
            'remaining_reps': remaining_reps
        })

    return render(request, 'habit_tracker/show_repetitions.html', {'habit_repetitions': habit_repetitions})

