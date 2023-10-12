# Standard library imports
from datetime import date, timedelta

# Third-party imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# Local application imports
from .forms import HabitForm
from .models import Habit, CheckOff


def welcome(request):
    return render(request, 'habit_tracker/welcome.html')

def create_example_habits(user):
    if Habit.objects.filter(user=user).count() == 0:
        # No habits found for this user, let's create some example habits

        # Create a habit that's already done due to time
        exercise_habit = Habit.objects.create(
            user=user,
            name="Exercise (Time Ended)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=30),
            completed=False
        )
        # Adding irregular check-offs, skipping some days
        for i in [0, 1, 3, 7, 14, 21, 28]:
            CheckOff.objects.create(
                habit=exercise_habit,
                timestamp=date.today() - timedelta(days=i)
            )


        # Create a habit that's fully completed
        habit2 = Habit.objects.create(
            user=user,
            name="Read Every Day (Fully Completed)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=30),
            completed=True
        )
        # Add check-offs for this habit
        for i in range(30):
            CheckOff.objects.create(
                habit=habit2,
                timestamp=date.today() - timedelta(days=i)
            )

        # Create a habit with a long streak of 365 days
        habit_long_streak = Habit.objects.create(
            user=user,
            name="Meditate (Long Streak)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=365),
            end_date=date.today(),
            completed=False
        )
        for i in range(365):
            CheckOff.objects.create(
                habit=habit_long_streak,
                timestamp=date.today() - timedelta(days=i)
            )

        # Create a habit with a short streak of 5 days
        habit_short_streak = Habit.objects.create(
            user=user,
            name="Learn Something New (Short Streak)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=5),
            end_date=date.today(),
            completed=False
        )
        for i in range(5):
            CheckOff.objects.create(
                habit=habit_short_streak,
                timestamp=date.today() - timedelta(days=i)
            )

        # Create a weekly habit for eating kebabs
        kebab_habit = Habit.objects.create(
            user=user,
            name="Eat Kebab :) (Weekly)",
            period=Habit.WEEKLY,
            start_date=date.today() - timedelta(weeks=4),
            end_date=date.today() + timedelta(weeks=4),
            completed=False
        )
        # Adding regular weekly check-offs
        for i in range(4):
            CheckOff.objects.create(
                habit=kebab_habit,
                timestamp=date.today() - timedelta(weeks=i)
            )

        # Create a monthly habit for connecting with loved ones
        connect_habit = Habit.objects.create(
            user=user,
            name="Connect with Loved Ones (Monthly)",
            period=Habit.MONTHLY,
            start_date=date.today() - timedelta(days=90),
            end_date=date.today() + timedelta(days=90),
            completed=False
        )
        # Adding regular monthly check-offs
        for i in range(3):
            CheckOff.objects.create(
                habit=connect_habit,
                timestamp=date.today() - timedelta(days=30*i)
            )


@login_required
def habit_list(request):
    create_example_habits(request.user)
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


@login_required
def show_streaks(request):
    # Step 1: Identify unique habits associated with the user
    user_habits = Habit.objects.filter(user=request.user)

    streaks_data = []
    
    for habit in user_habits:
        # Step 2: Fetch corresponding CheckOff records and sort them by timestamp
        checkoffs = CheckOff.objects.filter(habit=habit).order_by('timestamp')

        if checkoffs.exists():
            streak = 1  # Initialize streak to 1 as we have at least one checkoff
            prev_date = checkoffs.first().timestamp.date()

            for checkoff in checkoffs[1:]:
                curr_date = checkoff.timestamp.date()

                if (curr_date - prev_date).days == 1:
                    streak += 1
                else:
                    streak = 1  # Reset streak

                prev_date = curr_date

            # Step 3: Add the calculated streak to streaks_data
            streaks_data.append({'name': habit.name, 'streak': streak})

    # Sort the streaks_data by streak length
    sorted_streaks = sorted(streaks_data, key=lambda x: x['streak'], reverse=True)

    return render(request, 'habit_tracker/show_streaks.html', {'streaks': sorted_streaks})


@login_required
def show_repetitions(request):
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
            total_reps = total_days // 30  # Approximate days in a month
        
        # Calculate remaining repetitions
        done_reps = CheckOff.objects.filter(habit=habit).count()
        remaining_reps = total_reps - done_reps
        
        habit_repetitions.append({
            'name': habit.name,
            'total_reps': total_reps,
            'remaining_reps': remaining_reps
        })

    return render(request, 'habit_tracker/show_repetitions.html', {'habit_repetitions': habit_repetitions})


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



