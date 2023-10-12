from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_initial_users(sender, **kwargs):
    if User.objects.count() == 0:
        # Create superuser
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        # Create regular user
        User.objects.create_user('user', 'user@example.com', 'userpassword')
