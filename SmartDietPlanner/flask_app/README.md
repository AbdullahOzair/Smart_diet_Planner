# Smart Diet & Lifestyle Planner - Flask Application

A complete web application for managing diet and lifestyle planning with role-based authentication.

## 📁 Project Structure

```
flask_app/
│
├── app.py                    # Main Flask application with all routes
├── db.py                     # Database connection module
├── requirements.txt          # Python dependencies
│
├── templates/               # Jinja2 templates
│   ├── login.html           # Login page
│   ├── admin_dashboard.html # Admin dashboard with all features
│   └── user_dashboard.html  # User dashboard with logging features
│
└── static/                  # Static files
    └── style.css            # Custom CSS with health-themed design
```

## 🚀 Features

### Authentication
- Username/Password login
- Role-based access (Admin/User)
- Flask session management
- Secure logout

### Admin Features
- View all users
- View all daily logs
- View all meal logs
- View all activity logs
- View all user goals
- Add new meals to the database
- Add new activities to the database

### User Features
- View personal profile
- View personal goals
- Add daily logs (calories, water, sleep, weight)
- Add meal logs
- Add activity logs
- View AI suggestions

## 💾 Database Configuration

The application connects to Oracle Database (PDB):
- **User**: SYSTEM
- **Password**: system
- **DSN**: localhost:1521/XEPDB1

Update credentials in `db.py` if needed:
```python
DB_CONFIG = {
    'user': 'SYSTEM',
    'password': 'system',
    'dsn': 'localhost:1521/XEPDB1'
}
```

## 📋 Prerequisites

- Python 3.7+
- Oracle Database (with XEPDB1 PDB)
- Oracle Instant Client (for oracledb)

## 🔧 Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify database connection:**
   Make sure your Oracle database is running and accessible.

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and navigate to:
   ```
   http://localhost:5001
   ```

## 👤 Demo Credentials

### Admin Access
- **Username**: `zainab_moazzam` or `abdullah_ozair`
- **Password**: (use the password from your database)

### User Access
- **Username**: `test_user1`
- **Password**: `hashed_password_test1`

## 🎨 Design Features

- **Clean, modern UI** with Bootstrap 5
- **Health-inspired color palette** (greens, blues, soft tones)
- **Responsive design** for mobile and desktop
- **Card-based layout** for better organization
- **Smooth animations** and transitions
- **Icon integration** with Bootstrap Icons

## 📊 Database Tables Used

1. **USERS** - User account information
2. **GOALS** - User health goals
3. **DAILY_LOG** - Daily health metrics
4. **MEAL_LOG** - Meal consumption records
5. **ACTIVITY_LOG** - Physical activity records
6. **MOOD_LOG** - Mood tracking (future feature)
7. **MEALS** - Available meals database
8. **ACTIVITIES** - Available activities database
9. **SUGGESTIONS** - AI-generated suggestions
10. **REPORTS** - Generated reports (future feature)

## 🔐 Security Notes

⚠️ **For Production Use:**
- Change the Flask secret key in `app.py`
- Implement proper password hashing (bcrypt, argon2)
- Use environment variables for database credentials
- Enable HTTPS
- Add CSRF protection
- Implement rate limiting

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: Oracle Database (oracledb driver)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Templating**: Jinja2
- **Icons**: Bootstrap Icons

## 📱 Routes Overview

### Public Routes
- `/` - Redirect to login or dashboard
- `/login` - Login page
- `/logout` - Logout handler

### Admin Routes
- `/admin/dashboard` - Main admin dashboard
- `/admin/users` - View all users
- `/admin/daily-logs` - View all daily logs
- `/admin/meal-logs` - View all meal logs
- `/admin/activity-logs` - View all activity logs
- `/admin/goals` - View all goals
- `/admin/add-meal` - Add new meals
- `/admin/add-activity` - Add new activities

### User Routes
- `/user/dashboard` - Main user dashboard
- `/user/profile` - User profile
- `/user/goals` - User goals
- `/user/add-daily-log` - Add daily log
- `/user/add-meal-log` - Add meal log
- `/user/add-activity-log` - Add activity log
- `/user/suggestions` - View AI suggestions

## 🐛 Troubleshooting

### Database Connection Issues
- Verify Oracle database is running
- Check TNS configuration
- Ensure oracledb is properly installed
- Verify credentials in `db.py`

### Import Errors
- Install all dependencies: `pip install -r requirements.txt`
- Use virtual environment for clean installation

### Template Not Found
- Ensure templates are in `templates/` folder
- Check file names match route references

## 📄 License

This project is for educational purposes as part of a semester project.

## 👥 Authors

- Smart Diet Planner Development Team
- 7th Semester Project

## 📞 Support

For issues or questions, contact the development team.

---

**Note**: This is a complete, runnable application. No additional setup required beyond installing dependencies and configuring database credentials.
