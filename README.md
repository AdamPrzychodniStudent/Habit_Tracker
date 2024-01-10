# Habit Tracker Django Application
## Overview
The Habit Tracker is a Django web application designed to help users track and maintain their daily, weekly, and monthly habits. This application allows users to create habits, mark them as completed, view current habits, and observe progress over time.

## Features
- **Habit Creation:** Users can create new habits specifying the habit name, period (daily, weekly, monthly), start date, and end date.
- **Habit Tracking:** Track the completion of each habit with check-offs.
- **View Current Habits:** Display all current habits that are active and need attention.
- **Streaks & Struggles:** View the longest streaks for each habit and identify habits with which the user is struggling.
- **Automatic User Setup:** On initial deployment, the application sets up default users including an admin and a regular user.

## Technical Details
- **Django Models:** Includes models for Habit and CheckOff to store habit details and completion records.
- **Custom Forms:** Utilizes Django forms for input validation and clean data handling.
- **Signal Handling:** Implements Django signals to create initial users post-migration.
- **Automated Tests:** Contains tests for models, forms, and views ensuring robust application behavior.

##Running the Application in Gitpod
This application is configured to be easily set up and run in a Gitpod environment. When you start a Gitpod workspace with this repository, the environment sets up automatically, installing all the necessary dependencies and applying migrations to the database.

##Local Setup
To set up this application locally, follow these steps:

1. Clone the repository.
2. Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate  # Use venv\Scripts\activate on Windows
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Apply migrations to create the database schema:
```
python manage.py migrate
```
5. Run the development server:
```
python manage.py runserver
```
