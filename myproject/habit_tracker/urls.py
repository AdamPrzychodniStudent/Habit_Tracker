from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.create_habit, name='create_habit'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('current_habits/', views.show_current_habits, name='show_current_habits'),
    path('completed_habits/', views.show_completed_habits, name='show_completed_habits'),
    path('toggle_habit_done/<int:habit_id>/', views.toggle_habit_done, name='toggle_habit_done'),
]

