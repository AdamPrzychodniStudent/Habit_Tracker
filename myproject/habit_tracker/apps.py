from django.apps import AppConfig

# Define the configuration settings for the 'habit_tracker' app
class HabitTrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habit_tracker"

    # Overridden method that runs when the app is ready
    def ready(self):
        # Import signal configurations from 'habit_tracker.signals'
        import habit_tracker.signals

