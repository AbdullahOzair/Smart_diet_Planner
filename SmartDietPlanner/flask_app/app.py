"""
Smart Diet & Lifestyle Planner - Flask Application
Main application file with routes and business logic
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import oracledb
from db import get_db_connection, execute_query

# ============================================================================
# FLASK APP CONFIGURATION
# ============================================================================
app = Flask(__name__)
app.secret_key = 'smart_diet_planner_secret_key_2025'  # Change in production

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def authenticate_user(username, password):
    """
    Authenticate user credentials
    Returns: User data if valid, None otherwise
    """
    query = """
        SELECT user_id, username, email, first_name, last_name, 
            password_hash, gender, weight, height, activity_level
        FROM USERS 
        WHERE username = :username AND password_hash = :password
    """
    
    result = execute_query(query, {'username': username, 'password': password})
    
    if result and len(result) > 0:
        user = result[0]
        return {
            'user_id': user[0],
            'username': user[1],
            'email': user[2],
            'first_name': user[3],
            'last_name': user[4],
            'gender': user[6],
            'weight': user[7],
            'height': user[8],
            'activity_level': user[9]
        }
    return None


def check_admin(username):
    """
    Check if user has admin role
    Returns: True if admin, False otherwise
    """
    # For demo: hardcode admin usernames
    # In production, use a ROLE column in USERS table
    admin_usernames = ['admin', 'zainab_moazzam', 'abdullah_ozair']
    return username.lower() in admin_usernames


# ============================================================================
# ROUTES - AUTHENTICATION
# ============================================================================

@app.route('/')
def index():
    """Redirect to login page"""
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Authenticate user
        user = authenticate_user(username, password)
        
        if user:
            # Store user data in session
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['is_admin'] = check_admin(user['username'])
            
            flash('Login successful!', 'success')
            
            # Redirect based on role
            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        height = request.form.get('height')
        activity_level = request.form.get('activity_level')
        dietary_preference = request.form.get('dietary_preference', 'None')
        health_condition = request.form.get('health_condition', 'None')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        # Check if username already exists
        check_query = "SELECT user_id FROM USERS WHERE username = :username"
        existing_user = execute_query(check_query, {'username': username})
        
        if existing_user:
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        # Check if email already exists
        check_email = "SELECT user_id FROM USERS WHERE email = :email"
        existing_email = execute_query(check_email, {'email': email})
        
        if existing_email:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        # Insert new user
        insert_query = """
            INSERT INTO USERS (
                username, email, password_hash, first_name, last_name,
                date_of_birth, gender, weight, height, activity_level,
                dietary_preference, health_condition
            ) VALUES (
                :username, :email, :password, :first_name, :last_name,
                TO_DATE(:dob, 'YYYY-MM-DD'), :gender, :weight, :height, 
                :activity_level, :dietary_preference, :health_condition
            )
        """
        
        params = {
            'username': username,
            'email': email,
            'password': password,  # In production, hash this!
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'gender': gender,
            'weight': weight,
            'height': height,
            'activity_level': activity_level,
            'dietary_preference': dietary_preference,
            'health_condition': health_condition
        }
        
        if execute_query(insert_query, params, fetch=False):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')


# ============================================================================
# ROUTES - ADMIN DASHBOARD
# ============================================================================

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard - main view"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Get all statistics
    total_users = 0
    total_goals = 0
    total_meals = 0
    total_activities = 0
    total_logs = 0
    total_meal_logs = 0
    total_activity_logs = 0
    total_mood_logs = 0
    total_suggestions = 0
    total_reports = 0
    
    # Count users
    result = execute_query("SELECT COUNT(*) FROM USERS")
    if result:
        total_users = result[0][0]
    
    # Count goals
    result = execute_query("SELECT COUNT(*) FROM GOALS")
    if result:
        total_goals = result[0][0]
    
    # Count meals (master table)
    result = execute_query("SELECT COUNT(*) FROM MEALS")
    if result:
        total_meals = result[0][0]
    
    # Count activities (master table)
    result = execute_query("SELECT COUNT(*) FROM ACTIVITIES")
    if result:
        total_activities = result[0][0]
    
    # Count daily logs
    result = execute_query("SELECT COUNT(*) FROM DAILY_LOG")
    if result:
        total_logs = result[0][0]
    
    # Count meal logs
    result = execute_query("SELECT COUNT(*) FROM MEAL_LOG")
    if result:
        total_meal_logs = result[0][0]
    
    # Count activity logs
    result = execute_query("SELECT COUNT(*) FROM ACTIVITY_LOG")
    if result:
        total_activity_logs = result[0][0]
    
    # Count mood logs
    result = execute_query("SELECT COUNT(*) FROM MOOD_LOG")
    if result:
        total_mood_logs = result[0][0]
    
    # Count suggestions
    result = execute_query("SELECT COUNT(*) FROM SUGGESTIONS")
    if result:
        total_suggestions = result[0][0]
    
    # Count reports
    result = execute_query("SELECT COUNT(*) FROM REPORTS")
    if result:
        total_reports = result[0][0]
    
    # Get recent users for quick view
    recent_users = execute_query("""
        SELECT user_id, username, first_name, last_name, email,
               TO_CHAR(created_date, 'YYYY-MM-DD') as created
        FROM USERS ORDER BY created_date DESC FETCH FIRST 5 ROWS ONLY
    """)
    
    return render_template('admin_dashboard.html', 
                          total_users=total_users,
                          total_goals=total_goals,
                          total_meals=total_meals,
                          total_activities=total_activities,
                          total_logs=total_logs,
                          total_meal_logs=total_meal_logs,
                          total_activity_logs=total_activity_logs,
                          total_mood_logs=total_mood_logs,
                          total_suggestions=total_suggestions,
                          total_reports=total_reports,
                          recent_users=recent_users)


@app.route('/admin/users')
def admin_users():
    """Admin view all users with search and filter"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Get search and filter parameters
    search_name = request.args.get('search_name', '')
    filter_gender = request.args.get('filter_gender', '')
    filter_admin = request.args.get('filter_admin', '')
    
    query = """
        SELECT user_id, username, email, first_name, last_name, 
            gender, weight, height, activity_level,
            TO_CHAR(created_date, 'YYYY-MM-DD') as created
        FROM USERS 
        WHERE 1=1
    """
    
    params = {}
    
    # Apply search by name
    if search_name:
        query += " AND (UPPER(first_name) LIKE UPPER(:search) OR UPPER(last_name) LIKE UPPER(:search) OR UPPER(username) LIKE UPPER(:search))"
        params['search'] = f'%{search_name}%'
    
    # Apply gender filter
    if filter_gender:
        query += " AND gender = :gender"
        params['gender'] = filter_gender
    
    query += " ORDER BY user_id DESC"
    
    users = execute_query(query, params if params else None)
    
    return render_template('admin_dashboard.html', view='users', users=users,
                         search_name=search_name, filter_gender=filter_gender, filter_admin=filter_admin)


# User CRUD Operations (Create, Read, Update, Delete)
@app.route('/admin/user/view/<int:user_id>')
def admin_view_user(user_id):
    """View detailed information about a specific user"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT user_id, username, email, first_name, last_name, 
            TO_CHAR(date_of_birth, 'YYYY-MM-DD') as date_of_birth,
            gender, weight, height, activity_level,
            TO_CHAR(created_date, 'YYYY-MM-DD HH24:MI') as created
        FROM USERS 
        WHERE user_id = :user_id
    """
    
    user = execute_query(query, {'user_id': user_id})
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_users'))
    
    # Get user's goals
    goals_query = """
        SELECT goal_id, goal_type, target_value, current_value,
            TO_CHAR(start_date, 'YYYY-MM-DD') as start_date,
            TO_CHAR(target_date, 'YYYY-MM-DD') as target_date,
            status
        FROM GOALS
        WHERE user_id = :user_id
        ORDER BY start_date DESC
    """
    goals = execute_query(goals_query, {'user_id': user_id})
    
    # Get user's recent logs
    logs_query = """
        SELECT TO_CHAR(log_date, 'YYYY-MM-DD') as log_date,
            total_calories_consumed, total_calories_burned,
            water_intake, weight
        FROM DAILY_LOG
        WHERE user_id = :user_id
        ORDER BY log_date DESC
        FETCH FIRST 10 ROWS ONLY
    """
    logs = execute_query(logs_query, {'user_id': user_id})
    
    return render_template('admin_dashboard.html', view='view_user', user=user[0], goals=goals, logs=logs)


@app.route('/admin/user/create', methods=['GET', 'POST'])
def admin_create_user():
    """Create a new user account"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        height = request.form.get('height')
        activity_level = request.form.get('activity_level')
        
        # Check if username or email already exists
        check_query = "SELECT user_id FROM USERS WHERE username = :username OR email = :email"
        existing = execute_query(check_query, {'username': username, 'email': email})
        
        if existing:
            flash('Username or email already exists', 'error')
            return render_template('admin_dashboard.html', view='create_user')
        
        # Insert new user
        insert_query = """
            INSERT INTO USERS (username, email, password_hash, first_name, last_name,
                date_of_birth, gender, weight, height, activity_level)
            VALUES (:username, :email, :password, :first_name, :last_name,
                TO_DATE(:dob, 'YYYY-MM-DD'), :gender, :weight, :height, :activity_level)
        """
        
        params = {
            'username': username,
            'email': email,
            'password': password,  # In production, hash this password
            'first_name': first_name,
            'last_name': last_name,
            'dob': date_of_birth,
            'gender': gender,
            'weight': float(weight) if weight else None,
            'height': float(height) if height else None,
            'activity_level': activity_level
        }
        
        execute_query(insert_query, params, fetch=False)
        flash('User created successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin_dashboard.html', view='create_user')


@app.route('/admin/user/update/<int:user_id>', methods=['GET', 'POST'])
def admin_update_user(user_id):
    """Update user information"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        height = request.form.get('height')
        activity_level = request.form.get('activity_level')
        
        update_query = """
            UPDATE USERS SET
                email = :email,
                first_name = :first_name,
                last_name = :last_name,
                date_of_birth = TO_DATE(:dob, 'YYYY-MM-DD'),
                gender = :gender,
                weight = :weight,
                height = :height,
                activity_level = :activity_level
            WHERE user_id = :user_id
        """
        
        params = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'dob': date_of_birth,
            'gender': gender,
            'weight': float(weight) if weight else None,
            'height': float(height) if height else None,
            'activity_level': activity_level,
            'user_id': user_id
        }
        
        execute_query(update_query, params, fetch=False)
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    # GET request - fetch user data
    query = """
        SELECT user_id, username, email, first_name, last_name,
            TO_CHAR(date_of_birth, 'YYYY-MM-DD') as date_of_birth,
            gender, weight, height, activity_level
        FROM USERS 
        WHERE user_id = :user_id
    """
    
    user = execute_query(query, {'user_id': user_id})
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_users'))
    
    return render_template('admin_dashboard.html', view='update_user', user=user[0])


@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    """Delete a user account"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    # Prevent admin from deleting themselves
    if user_id == session['user_id']:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('admin_users'))
    
    # Delete user (cascade will handle related records)
    delete_query = "DELETE FROM USERS WHERE user_id = :user_id"
    execute_query(delete_query, {'user_id': user_id}, fetch=False)
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/daily-logs')
def admin_daily_logs():
    """Admin view all daily logs"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT d.daily_log_id, u.username, 
               TO_CHAR(d.log_date, 'YYYY-MM-DD') as log_date,
               d.total_calories_consumed, d.total_calories_burned,
               d.water_intake, d.sleep_hours, d.weight
        FROM DAILY_LOG d
        JOIN USERS u ON d.user_id = u.user_id
        ORDER BY d.log_date DESC
        FETCH FIRST 50 ROWS ONLY
    """
    
    logs = execute_query(query)
    return render_template('admin_dashboard.html', view='daily_logs', daily_logs=logs)


@app.route('/admin/meal-logs')
def admin_meal_logs():
    """Admin view all meal logs"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT ml.meal_log_id, u.username, m.meal_name,
               TO_CHAR(ml.meal_time, 'YYYY-MM-DD HH24:MI') as meal_time,
               ml.quantity, ml.total_calories
        FROM MEAL_LOG ml
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        JOIN USERS u ON d.user_id = u.user_id
        JOIN MEALS m ON ml.meal_id = m.meal_id
        ORDER BY ml.meal_time DESC
        FETCH FIRST 50 ROWS ONLY
    """
    
    meal_logs = execute_query(query)
    return render_template('admin_dashboard.html', view='meal_logs', meal_logs=meal_logs)


@app.route('/admin/activity-logs')
def admin_activity_logs():
    """Admin view all activity logs"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT al.activity_log_id, u.username, a.activity_name,
               TO_CHAR(al.activity_time, 'YYYY-MM-DD HH24:MI') as activity_time,
               al.duration_minutes, al.calories_burned
        FROM ACTIVITY_LOG al
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        JOIN USERS u ON d.user_id = u.user_id
        JOIN ACTIVITIES a ON al.activity_id = a.activity_id
        ORDER BY al.activity_time DESC
        FETCH FIRST 50 ROWS ONLY
    """
    
    activity_logs = execute_query(query)
    return render_template('admin_dashboard.html', view='activity_logs', activity_logs=activity_logs)


@app.route('/admin/goals')
def admin_goals():
    """Admin view all goals"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT g.goal_id, u.username, g.goal_type, 
               g.target_value, g.current_value, g.status,
               TO_CHAR(g.start_date, 'YYYY-MM-DD') as start_date,
               TO_CHAR(g.target_date, 'YYYY-MM-DD') as target_date
        FROM GOALS g
        JOIN USERS u ON g.user_id = u.user_id
        ORDER BY g.created_date DESC
    """
    
    goals = execute_query(query)
    return render_template('admin_dashboard.html', view='goals', goals=goals)


@app.route('/admin/add-meal', methods=['GET', 'POST'])
def admin_add_meal():
    """Admin add new meal"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        meal_name = request.form.get('meal_name')
        meal_category = request.form.get('meal_category')
        calories = request.form.get('calories')
        protein = request.form.get('protein')
        carbs = request.form.get('carbs')
        fats = request.form.get('fats')
        
        query = """
            INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats)
            VALUES (:meal_name, :meal_category, :calories, :protein, :carbs, :fats)
        """
        
        params = {
            'meal_name': meal_name,
            'meal_category': meal_category,
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fats': fats
        }
        
        if execute_query(query, params, fetch=False):
            flash('Meal added successfully!', 'success')
        else:
            flash('Failed to add meal', 'error')
        
        return redirect(url_for('admin_add_meal'))
    
    # Get all meals
    meals = execute_query("SELECT * FROM MEALS ORDER BY meal_id DESC")
    return render_template('admin_dashboard.html', view='add_meal', meals=meals)


@app.route('/admin/add-activity', methods=['GET', 'POST'])
def admin_add_activity():
    """Admin add new activity"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        activity_name = request.form.get('activity_name')
        activity_category = request.form.get('activity_category')
        calories_per_minute = request.form.get('calories_per_minute')
        intensity_level = request.form.get('intensity_level', 'Moderate')
        
        query = """
            INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level)
            VALUES (:activity_name, :activity_category, :calories_per_minute, :intensity_level)
        """
        
        params = {
            'activity_name': activity_name,
            'activity_category': activity_category,
            'calories_per_minute': calories_per_minute,
            'intensity_level': intensity_level
        }
        
        if execute_query(query, params, fetch=False):
            flash('Activity added successfully!', 'success')
        else:
            flash('Failed to add activity', 'error')
        
        return redirect(url_for('admin_add_activity'))
    
    # Get all activities
    activities = execute_query("SELECT * FROM ACTIVITIES ORDER BY activity_id DESC")
    return render_template('admin_dashboard.html', view='add_activity', activities=activities)


@app.route('/admin/suggestions')
def admin_suggestions():
    """Admin view all suggestions"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT s.suggestion_id, u.username, s.suggestion_type, s.suggestion_text,
               s.reasoning, s.priority, s.status,
               TO_CHAR(s.created_date, 'YYYY-MM-DD HH24:MI') as created_date
        FROM SUGGESTIONS s
        JOIN USERS u ON s.user_id = u.user_id
        ORDER BY s.created_date DESC
    """
    
    suggestions = execute_query(query)
    return render_template('admin_dashboard.html', view='suggestions', suggestions=suggestions)


@app.route('/admin/reports')
def admin_reports():
    """Admin view all reports"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT r.report_id, u.username, r.report_type,
               TO_CHAR(r.report_period_start, 'YYYY-MM-DD') as period_start,
               TO_CHAR(r.report_period_end, 'YYYY-MM-DD') as period_end,
               r.total_calories_consumed, r.total_calories_burned,
               r.average_weight, r.weight_change, r.goals_achieved,
               r.report_summary,
               TO_CHAR(r.generated_date, 'YYYY-MM-DD HH24:MI') as generated_date
        FROM REPORTS r
        JOIN USERS u ON r.user_id = u.user_id
        ORDER BY r.generated_date DESC
    """
    
    reports = execute_query(query)
    return render_template('admin_dashboard.html', view='reports', reports=reports)


@app.route('/admin/mood-logs')
def admin_mood_logs():
    """Admin view all mood logs"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT m.mood_log_id, u.username, m.mood_rating,
               m.stress_level, m.energy_level, m.notes,
               TO_CHAR(m.log_time, 'YYYY-MM-DD HH24:MI') as log_time
        FROM MOOD_LOG m
        JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
        JOIN USERS u ON d.user_id = u.user_id
        ORDER BY m.log_time DESC
    """
    
    mood_logs = execute_query(query)
    return render_template('admin_dashboard.html', view='mood_logs', mood_logs=mood_logs)


@app.route('/admin/meals')
def admin_meals():
    """Admin view all meals (master table)"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT meal_id, meal_name, meal_category, calories, 
               protein, carbohydrates, fats, fiber, serving_size, description
        FROM MEALS ORDER BY meal_id
    """
    
    meals = execute_query(query)
    return render_template('admin_dashboard.html', view='meals', meals=meals)


@app.route('/admin/activities')
def admin_activities():
    """Admin view all activities (master table)"""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    query = """
        SELECT activity_id, activity_name, activity_category, 
               calories_per_minute, intensity_level, description
        FROM ACTIVITIES ORDER BY activity_id
    """
    
    activities = execute_query(query)
    return render_template('admin_dashboard.html', view='activities', activities=activities)


# ============================================================================
# ROUTES - USER DASHBOARD
# ============================================================================

@app.route('/user/dashboard')
def user_dashboard():
    """User dashboard - main view"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get user statistics
    stats = {
        'total_logs': 0,
        'total_meals': 0,
        'total_activities': 0,
        'active_goals': 0
    }
    
    # Count daily logs
    result = execute_query("SELECT COUNT(*) FROM DAILY_LOG WHERE user_id = :user_id", {'user_id': user_id})
    if result:
        stats['total_logs'] = result[0][0]
    
    # Count meal logs (through DAILY_LOG since MEAL_LOG has no user_id)
    result = execute_query("""
        SELECT COUNT(*) FROM MEAL_LOG ml 
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id 
        WHERE d.user_id = :user_id
    """, {'user_id': user_id})
    if result:
        stats['total_meals'] = result[0][0]
    
    # Count activity logs (through DAILY_LOG since ACTIVITY_LOG has no user_id)
    result = execute_query("""
        SELECT COUNT(*) FROM ACTIVITY_LOG al 
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id 
        WHERE d.user_id = :user_id
    """, {'user_id': user_id})
    if result:
        stats['total_activities'] = result[0][0]
    
    # Count active goals
    result = execute_query("SELECT COUNT(*) FROM GOALS WHERE user_id = :user_id AND status = 'Active'", {'user_id': user_id})
    if result:
        stats['active_goals'] = result[0][0]
    
    return render_template('user_dashboard.html', stats=stats)


@app.route('/user/profile')
def user_profile():
    """User view own profile"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    query = """
        SELECT user_id, username, email, first_name, last_name,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob,
               gender, weight, height, activity_level, 
               dietary_preference, health_condition,
               TO_CHAR(created_date, 'YYYY-MM-DD') as created
        FROM USERS 
        WHERE user_id = :user_id
    """
    
    result = execute_query(query, {'user_id': user_id})
    profile = result[0] if result else None
    
    return render_template('user_dashboard.html', view='profile', profile=profile)


@app.route('/user/goals')
def user_goals():
    """User view own goals"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    query = """
        SELECT goal_id, goal_type, target_value, current_value, status,
               TO_CHAR(start_date, 'YYYY-MM-DD') as start_date,
               TO_CHAR(target_date, 'YYYY-MM-DD') as target_date
        FROM GOALS 
        WHERE user_id = :user_id
        ORDER BY created_date DESC
    """
    
    goals = execute_query(query, {'user_id': user_id})
    return render_template('user_dashboard.html', view='goals', goals=goals)


@app.route('/user/add-goal', methods=['GET', 'POST'])
def user_add_goal():
    """User add new goal"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        goal_type = request.form.get('goal_type')
        target_value = request.form.get('target_value')
        current_value = request.form.get('current_value')
        target_date = request.form.get('target_date')
        
        query = """
            INSERT INTO GOALS (user_id, goal_type, target_value, current_value, target_date, start_date, status)
            VALUES (:user_id, :goal_type, :target_value, :current_value, 
                    TO_DATE(:target_date, 'YYYY-MM-DD'), SYSDATE, 'Active')
        """
        
        params = {
            'user_id': user_id,
            'goal_type': goal_type,
            'target_value': target_value,
            'current_value': current_value,
            'target_date': target_date
        }
        
        try:
            if execute_query(query, params, fetch=False):
                flash('Goal created successfully!', 'success')
                return redirect(url_for('user_goals'))
            else:
                flash('Failed to create goal', 'error')
        except Exception as e:
            flash(f'Error creating goal: {str(e)}', 'error')
    
    return render_template('user_dashboard.html', view='add_goal')


@app.route('/user/add-daily-log', methods=['GET', 'POST'])
def user_add_daily_log():
    """User add daily log"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        log_date = request.form.get('log_date')
        calories_consumed = request.form.get('calories_consumed')
        calories_burned = request.form.get('calories_burned')
        water_intake = request.form.get('water_intake')
        sleep_hours = request.form.get('sleep_hours')
        weight = request.form.get('weight')
        
        query = """
            INSERT INTO DAILY_LOG 
            (user_id, log_date, total_calories_consumed, total_calories_burned, 
             water_intake, sleep_hours, weight)
            VALUES (:user_id, TO_DATE(:log_date, 'YYYY-MM-DD'), 
                    :calories_consumed, :calories_burned, 
                    :water_intake, :sleep_hours, :weight)
        """
        
        params = {
            'user_id': user_id,
            'log_date': log_date,
            'calories_consumed': calories_consumed,
            'calories_burned': calories_burned,
            'water_intake': water_intake,
            'sleep_hours': sleep_hours,
            'weight': weight
        }
        
        if execute_query(query, params, fetch=False):
            flash('Daily log added successfully!', 'success')
        else:
            flash('Failed to add daily log', 'error')
        
        return redirect(url_for('user_add_daily_log'))
    
    # Get recent logs
    user_id = session['user_id']
    logs = execute_query("""
        SELECT daily_log_id, TO_CHAR(log_date, 'YYYY-MM-DD') as log_date,
               total_calories_consumed, total_calories_burned,
               water_intake, sleep_hours, weight
        FROM DAILY_LOG 
        WHERE user_id = :user_id
        ORDER BY log_date DESC
        FETCH FIRST 10 ROWS ONLY
    """, {'user_id': user_id})
    
    return render_template('user_dashboard.html', view='add_daily_log', daily_logs=logs)


@app.route('/user/add-meal-log', methods=['GET', 'POST'])
def user_add_meal_log():
    """User add meal log"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        meal_id = request.form.get('meal_id')
        meal_time = request.form.get('meal_time')
        quantity = request.form.get('quantity')
        
        # Validate inputs
        if not meal_id or not meal_time or not quantity:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('user_add_meal_log'))
        
        # Convert datetime-local format (2025-12-18T14:30) to Oracle format
        if meal_time:
            meal_time = meal_time.replace('T', ' ')
        
        try:
            # Get meal calories
            meal_result = execute_query("SELECT calories FROM MEALS WHERE meal_id = :meal_id", {'meal_id': meal_id})
            
            if not meal_result or len(meal_result) == 0:
                flash('Selected meal not found', 'error')
                return redirect(url_for('user_add_meal_log'))
            
            total_calories = float(meal_result[0][0]) * float(quantity)
            
            # Get or create daily log for today
            today_log = execute_query("""
                SELECT daily_log_id FROM DAILY_LOG 
                WHERE user_id = :user_id AND log_date = TRUNC(SYSDATE)
            """, {'user_id': user_id})
            
            if not today_log:
                # Create daily log for today
                create_result = execute_query("""
                    INSERT INTO DAILY_LOG (user_id, log_date) 
                    VALUES (:user_id, TRUNC(SYSDATE))
                """, {'user_id': user_id}, fetch=False)
                
                if not create_result:
                    flash('Failed to create daily log', 'error')
                    return redirect(url_for('user_add_meal_log'))
                
                today_log = execute_query("""
                    SELECT daily_log_id FROM DAILY_LOG 
                    WHERE user_id = :user_id AND log_date = TRUNC(SYSDATE)
                """, {'user_id': user_id})
            
            daily_log_id = today_log[0][0] if today_log else None
            
            if not daily_log_id:
                flash('Failed to get daily log ID', 'error')
                return redirect(url_for('user_add_meal_log'))
            
            # Insert meal log
            query = """
                INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories)
                VALUES (:daily_log_id, :meal_id, 
                        TO_TIMESTAMP(:meal_time, 'YYYY-MM-DD HH24:MI'), 
                        :quantity, :total_calories)
            """
            
            params = {
                'daily_log_id': daily_log_id,
                'meal_id': meal_id,
                'meal_time': meal_time,
                'quantity': quantity,
                'total_calories': total_calories
            }
        
            result = execute_query(query, params, fetch=False)
            if result:
                flash('Meal log added successfully!', 'success')
            else:
                flash('Failed to add meal log - database error', 'error')
                
        except ValueError as e:
            flash(f'Invalid number format: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error adding meal log: {str(e)}', 'error')
        
        return redirect(url_for('user_add_meal_log'))
    
    # Get all meals
    meals = execute_query("SELECT meal_id, meal_name, meal_category, calories FROM MEALS ORDER BY meal_name")
    
    # Get recent meal logs (through DAILY_LOG since MEAL_LOG has no user_id)
    user_id = session['user_id']
    meal_logs = execute_query("""
        SELECT ml.meal_log_id, m.meal_name,
               TO_CHAR(ml.meal_time, 'YYYY-MM-DD HH24:MI') as meal_time,
               ml.quantity, ml.total_calories
        FROM MEAL_LOG ml
        JOIN MEALS m ON ml.meal_id = m.meal_id
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        WHERE d.user_id = :user_id
        ORDER BY ml.meal_time DESC
        FETCH FIRST 10 ROWS ONLY
    """, {'user_id': user_id})
    
    return render_template('user_dashboard.html', view='add_meal_log', meals=meals, meal_logs=meal_logs)


@app.route('/user/add-activity-log', methods=['GET', 'POST'])
def user_add_activity_log():
    """User add activity log"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        activity_id = request.form.get('activity_id')
        activity_time = request.form.get('activity_time')
        duration = request.form.get('duration')
        
        # Convert datetime-local format (2025-12-18T14:30) to Oracle format
        if activity_time:
            activity_time = activity_time.replace('T', ' ')
        
        # Get activity calories per minute
        activity_result = execute_query("SELECT calories_per_minute FROM ACTIVITIES WHERE activity_id = :activity_id", 
                                        {'activity_id': activity_id})
        
        if activity_result:
            calories_per_minute = float(activity_result[0][0])
            calories_burned = calories_per_minute * float(duration)
            
            # Get or create daily log for today
            today_log = execute_query("""
                SELECT daily_log_id FROM DAILY_LOG 
                WHERE user_id = :user_id AND log_date = TRUNC(SYSDATE)
            """, {'user_id': user_id})
            
            if not today_log:
                # Create daily log for today
                execute_query("""
                    INSERT INTO DAILY_LOG (user_id, log_date) 
                    VALUES (:user_id, TRUNC(SYSDATE))
                """, {'user_id': user_id}, fetch=False)
                today_log = execute_query("""
                    SELECT daily_log_id FROM DAILY_LOG 
                    WHERE user_id = :user_id AND log_date = TRUNC(SYSDATE)
                """, {'user_id': user_id})
            
            daily_log_id = today_log[0][0] if today_log else None
            
            if daily_log_id:
                try:
                    query = """
                        INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, activity_time, duration_minutes, calories_burned)
                        VALUES (:daily_log_id, :activity_id, 
                                TO_TIMESTAMP(:activity_time, 'YYYY-MM-DD HH24:MI'), 
                                :duration_minutes, :calories_burned)
                    """
                    
                    params = {
                        'daily_log_id': daily_log_id,
                        'activity_id': activity_id,
                        'activity_time': activity_time,
                        'duration_minutes': duration,
                        'calories_burned': calories_burned
                    }
                
                    if execute_query(query, params, fetch=False):
                        flash('Activity log added successfully!', 'success')
                    else:
                        flash('Failed to add activity log', 'error')
                except Exception as e:
                    flash(f'Error adding activity log: {str(e)}', 'error')
            else:
                flash('Failed to create daily log', 'error')
        
        return redirect(url_for('user_add_activity_log'))
    
    # Get all activities
    activities = execute_query("SELECT activity_id, activity_name, activity_category, calories_per_minute FROM ACTIVITIES ORDER BY activity_name")
    
    # Get recent activity logs (through DAILY_LOG since ACTIVITY_LOG has no user_id)
    user_id = session['user_id']
    activity_logs = execute_query("""
        SELECT al.activity_log_id, a.activity_name,
               TO_CHAR(al.activity_time, 'YYYY-MM-DD HH24:MI') as activity_time,
               al.duration_minutes, al.calories_burned
        FROM ACTIVITY_LOG al
        JOIN ACTIVITIES a ON al.activity_id = a.activity_id
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = :user_id
        ORDER BY al.activity_time DESC
        FETCH FIRST 10 ROWS ONLY
    """, {'user_id': user_id})
    
    return render_template('user_dashboard.html', view='add_activity_log', 
                          activities=activities, activity_logs=activity_logs)


@app.route('/user/suggestions')
def user_suggestions():
    """User view AI suggestions"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    query = """
        SELECT suggestion_id, suggestion_type, suggestion_text,
               TO_CHAR(created_date, 'YYYY-MM-DD HH24:MI') as created
        FROM SUGGESTIONS 
        WHERE user_id = :user_id
        ORDER BY created_date DESC
    """
    
    suggestions = execute_query(query, {'user_id': user_id})
    return render_template('user_dashboard.html', view='suggestions', suggestions=suggestions)


@app.route('/user/add-mood-log', methods=['GET', 'POST'])
def user_add_mood_log():
    """User add mood log (stress, energy levels)"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        mood_rating = request.form.get('mood_rating')
        stress_level_num = request.form.get('stress_level')
        energy_level_num = request.form.get('energy_level')
        notes = request.form.get('notes', '')
        
        # Convert numeric levels to text (only Low, Moderate, High allowed by DB)
        level_map = {
            '1': 'Low', '2': 'Low', '3': 'Low',
            '4': 'Moderate', '5': 'Moderate', '6': 'Moderate', '7': 'Moderate',
            '8': 'High', '9': 'High', '10': 'High'
        }
        stress_level = level_map.get(stress_level_num, 'Moderate')
        energy_level = level_map.get(energy_level_num, 'Moderate')
        
        # Get or create daily log for today
        today_log = execute_query("""
            SELECT daily_log_id FROM DAILY_LOG 
            WHERE user_id = :user_id AND log_date = TRUNC(SYSDATE)
        """, {'user_id': user_id})
        
        if not today_log:
            # Create daily log for today
            execute_query("""
                INSERT INTO DAILY_LOG (user_id, log_date) 
                VALUES (:user_id, TRUNC(SYSDATE))
            """, {'user_id': user_id}, fetch=False)
            today_log = execute_query("""
                SELECT daily_log_id FROM DAILY_LOG 
                WHERE user_id = :user_id AND log_date = TRUNC(SYSDATE)
            """, {'user_id': user_id})
        
        daily_log_id = today_log[0][0] if today_log else None
        
        if daily_log_id:
            try:
                query = """
                    INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
                    VALUES (:daily_log_id, :mood_rating, :stress_level, :energy_level, :notes, CURRENT_TIMESTAMP)
                """
                
                params = {
                    'daily_log_id': daily_log_id,
                    'mood_rating': mood_rating,
                    'stress_level': stress_level,
                    'energy_level': energy_level,
                    'notes': notes
                }
                
                if execute_query(query, params, fetch=False):
                    flash('Mood log added successfully!', 'success')
                else:
                    flash('Failed to add mood log', 'error')
            except Exception as e:
                flash(f'Error adding mood log: {str(e)}', 'error')
        else:
            flash('Failed to create daily log', 'error')
        
        return redirect(url_for('user_add_mood_log'))
    
    # Get recent mood logs (through DAILY_LOG since MOOD_LOG has no user_id)
    user_id = session['user_id']
    mood_logs = execute_query("""
        SELECT m.mood_log_id, TO_CHAR(m.log_time, 'YYYY-MM-DD HH24:MI') as log_time,
               m.mood_rating, m.stress_level, m.energy_level, m.notes
        FROM MOOD_LOG m
        JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = :user_id
        ORDER BY m.log_time DESC
        FETCH FIRST 10 ROWS ONLY
    """, {'user_id': user_id})
    
    return render_template('user_dashboard.html', view='add_mood_log', mood_logs=mood_logs)


@app.route('/user/reports')
def user_reports():
    """User view their reports"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    query = """
        SELECT report_id, report_type,
               TO_CHAR(report_period_start, 'YYYY-MM-DD') as period_start,
               TO_CHAR(report_period_end, 'YYYY-MM-DD') as period_end,
               total_calories_consumed, total_calories_burned,
               average_weight, weight_change, goals_achieved,
               report_summary,
               TO_CHAR(generated_date, 'YYYY-MM-DD HH24:MI') as generated_date
        FROM REPORTS 
        WHERE user_id = :user_id
        ORDER BY generated_date DESC
    """
    
    reports = execute_query(query, {'user_id': user_id})
    return render_template('user_dashboard.html', view='reports', reports=reports)


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
