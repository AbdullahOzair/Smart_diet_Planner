# Smart Diet & Lifestyle Planner - User Guide

## Application URL
**http://127.0.0.1:5001**

## Demo Credentials

### Admin Users
1. **Username:** zainab_moazzam  
   **Password:** hashed_password_123  
   **Role:** Admin

2. **Username:** abdullah_ozair  
   **Password:** hashed_password_456  
   **Role:** Admin

### Regular Users
1. **Username:** test_user1  
   **Password:** hashed_password_test1  
   **Role:** User

2. **Username:** test_user2  
   **Password:** hashed_password_test2  
   **Role:** User

## Features

### Registration & Login ✓
- New user registration with email validation
- Duplicate username/email checking
- Password and confirm password validation
- Secure login system with session management

### User Dashboard Features ✓

1. **Dashboard Overview**
   - View today's nutrition summary
   - Track calories, protein, carbs, fats
   - View recent activities
   - Progress towards daily goals

2. **My Profile**
   - View and edit personal information
   - Update health metrics (weight, height, BMI)
   - Manage account details

3. **My Goals**
   - View current health goals
   - Track goal progress
   - Update goal targets

4. **Add Daily Log**
   - Log daily calorie intake
   - Track water consumption
   - Monitor weight changes

5. **Add Meal Log**
   - Log meals from predefined meal database
   - Record meal time and portion size
   - Track nutritional values

6. **Add Activity Log**
   - Log physical activities
   - Track duration and calories burned
   - View activity history

7. **Add Mood Log** ✓ (NEW)
   - Log daily mood (Very Happy to Very Sad)
   - Track stress levels (1-10 scale)
   - Monitor energy levels (1-10 scale)
   - Add optional notes about your day

8. **AI Suggestions**
   - Receive personalized health suggestions
   - Based on your logging patterns
   - Diet and lifestyle recommendations

### Admin Dashboard Features ✓

1. **Admin Overview**
   - View total users statistics
   - Monitor system activity
   - Access analytics

2. **Manage Users**
   - View all registered users
   - Edit user information
   - Manage user accounts

3. **Daily Logs Management**
   - View all user daily logs
   - Monitor calorie intake patterns
   - Track user progress

4. **Meal Logs Management**
   - View all meal logs
   - Analyze eating patterns
   - Monitor nutrition data

5. **Activity Logs Management**
   - View all activity logs
   - Track user exercise patterns
   - Monitor calories burned

6. **Goals Management**
   - View all user goals
   - Monitor goal progress
   - Track achievement rates

7. **Add Meals to Database**
   - Add new meals to the system
   - Define nutritional values
   - Categorize meals

8. **Add Activities to Database**
   - Add new activities
   - Define calorie burn rates
   - Categorize activities

## Functional Requirements Status

✓ = Implemented | ⚠ = Partial | ✗ = Not Implemented

1. ✓ User Registration and Login
2. ✓ Role-based Access Control (Admin/User)
3. ✓ Log Daily Calorie Intake
4. ✓ Record Physical Activities
5. ✓ Log Mood, Stress, and Energy Levels
6. ✓ View AI-Generated Suggestions
7. ✓ Admin: Manage Users
8. ✓ Admin: View All Logs
9. ✓ Admin: Add Meals/Activities
10. ⚠ Generate Reports (Basic reporting available, advanced reports pending)
11. ✓ Data Integrity (Database constraints and triggers)
12. ⚠ Backup and Recovery (Database-level features configured)

## How to Use

### For New Users:
1. Visit http://127.0.0.1:5001
2. Click "Create New Account" on the login page
3. Fill in the registration form with:
   - Username, Email, Password
   - Personal info (name, age, gender)
   - Health metrics (weight, height, activity level)
4. Click "Create Account"
5. Login with your new credentials

### For Existing Users:
1. Visit http://127.0.0.1:5001
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to your dashboard based on your role

### Logging Your Health Data:
1. **Daily Log:** Track overall calories and water intake
2. **Meal Log:** Record specific meals with nutritional info
3. **Activity Log:** Log exercises and activities
4. **Mood Log:** Track your mental and emotional well-being

### Viewing Suggestions:
- Navigate to "AI Suggestions" in the sidebar
- View personalized recommendations based on your logs

## Technical Details

- **Framework:** Flask 3.0.0
- **Database:** Oracle Database 21c (XEPDB1)
- **Frontend:** Bootstrap 5.3.0 + Custom CSS
- **Python:** 3.13.1
- **Port:** 5001 (Development Server)

## Support

For issues or questions, check:
- README.md for setup instructions
- Database schema in database/create_tables.sql
- Application code in flask_app/app.py

---
**Note:** This is a development server. For production use, deploy with a production WSGI server like Gunicorn or uWSGI.
