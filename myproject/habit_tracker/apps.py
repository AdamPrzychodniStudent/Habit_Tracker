from django.apps import AppConfig


class HabitTrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habit_tracker"

    def ready(self):
        import habit_tracker.signals
