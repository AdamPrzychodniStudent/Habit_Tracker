

from .models import Habit, CheckOff

from datetime import date, timedelta, datetime
from django.utils import timezone


# Helper function to update timestamp
def update_timestamp(checkoff, days_ago):
    naive_datetime = datetime.combine(date.today() - timedelta(days=days_ago), datetime.min.time())
    checkoff.timestamp = timezone.make_aware(naive_datetime)
    checkoff.save(update_fields=['timestamp'])


# Function to create example habits for a user
def create_example_habits(user):
    """
    Creates example habits for a new user.

    :param user: User object
    :return: None
    """
    if Habit.objects.filter(user=user).count() == 0:

        # DEFAULT HABIT EXAMPLES
        exercise_habit = Habit.objects.create(
            user=user,
            name="Exercise (Time Ended)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() - timedelta(days=1),
            completed=False
        )
        for i in [0, 1, 3, 7, 14, 21, 28]:
            checkoff = CheckOff.objects.create(habit=exercise_habit)
            update_timestamp(checkoff, i)

        habit2 = Habit.objects.create(
            user=user,
            name="Read Every Day (Fully Completed)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=30),
            completed=True
        )
        for i in range(30):
            checkoff = CheckOff.objects.create(habit=habit2)
            update_timestamp(checkoff, i)

        habit_long_streak = Habit.objects.create(
            user=user,
            name="Meditate (Long Streak)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=365),
            end_date=date.today(),
            completed=False
        )
        for i in range(365):
            checkoff = CheckOff.objects.create(habit=habit_long_streak)
            update_timestamp(checkoff, i)

        habit_short_streak = Habit.objects.create(
            user=user,
            name="Learn Something New (Short Streak)",
            period=Habit.DAILY,
            start_date=date.today() - timedelta(days=5),
            end_date=date.today(),
            completed=False
        )
        for i in range(1, 5):
            checkoff = CheckOff.objects.create(habit=habit_short_streak)
            update_timestamp(checkoff, i)

        kebab_habit = Habit.objects.create(
            user=user,
            name="Eat Kebab :) (Weekly)",
            period=Habit.WEEKLY,
            start_date=date.today() - timedelta(weeks=4),
            end_date=date.today() + timedelta(weeks=4),
            completed=False
        )
        for i in range(1, 4):
            checkoff = CheckOff.objects.create(habit=kebab_habit)
            update_timestamp(checkoff, 7*i)  

        connect_habit = Habit.objects.create(
            user=user,
            name="Connect with Loved Ones (Monthly)",
            period=Habit.MONTHLY,
            start_date=date.today() - timedelta(days=90),
            end_date=date.today() + timedelta(days=90),
            completed=False
        )
        for i in range(3):
            checkoff = CheckOff.objects.create(habit=connect_habit)
            update_timestamp(checkoff, 30*i)