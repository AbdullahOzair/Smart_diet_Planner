"""
Smart Diet & Lifestyle Planner - Flask Application
Main application file with routes and business logic
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, date
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
        WHERE username = %(username)s AND password_hash = %(password)s
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


def generate_ai_plan(profile, user_id, goal='maintain'):
    """Generate a personalized AI diet plan based on user profile and recent data."""
    from datetime import date as _date

    # --- BMI ---
    bmi, bmi_category = None, 'Normal'
    if profile and profile.get('weight') and profile.get('height'):
        w = float(profile['weight']); h_m = float(profile['height']) / 100
        bmi = round(w / (h_m * h_m), 1)
        bmi_category = 'Underweight' if bmi < 18.5 else ('Normal' if bmi < 25 else ('Overweight' if bmi < 30 else 'Obese'))

    # --- Calorie target via Mifflin-St Jeor ---
    calorie_target = 2000
    if profile:
        w = float(profile.get('weight') or 70)
        h_cm = float(profile.get('height') or 170)
        gender = (profile.get('gender') or 'male').lower()
        dob = profile.get('date_of_birth')
        age = 30
        try:
            today = _date.today()
            if hasattr(dob, 'year'):
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            elif dob:
                from datetime import datetime as _dt
                d = _dt.strptime(str(dob)[:10], '%Y-%m-%d').date()
                age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
        except Exception:
            age = 30
        bmr = (10*w + 6.25*h_cm - 5*age + 5) if gender == 'male' else (10*w + 6.25*h_cm - 5*age - 161)
        multiplier = {'Sedentary':1.2,'Light':1.375,'Moderate':1.55,'Active':1.725,'Very Active':1.9}.get(profile.get('activity_level','Sedentary'), 1.2)
        tdee = int(bmr * multiplier)
        calorie_target = max(1200, tdee - 500) if goal == 'weight_loss' else (tdee + 500 if goal == 'weight_gain' else tdee)

    # --- Meal plan ---
    mp = {
        'weight_loss': {
            'breakfast': {'name':'Oatmeal + Mixed Berries + Boiled Egg','calories':int(calorie_target*0.22),'icon':'🥣'},
            'lunch':     {'name':'Grilled Chicken + Brown Rice + Garden Salad','calories':int(calorie_target*0.35),'icon':'🍗'},
            'dinner':    {'name':'Vegetable Soup + Whole Wheat Bread','calories':int(calorie_target*0.28),'icon':'🥣'},
            'snacks':    {'name':'Greek Yogurt + Almonds','calories':int(calorie_target*0.15),'icon':'🥜'},
        },
        'weight_gain': {
            'breakfast': {'name':'Scrambled Eggs + Toast + Banana + Full-fat Milk','calories':int(calorie_target*0.25),'icon':'🍳'},
            'lunch':     {'name':'Beef + White Rice + Beans + Cheese','calories':int(calorie_target*0.35),'icon':'🥩'},
            'dinner':    {'name':'Salmon + Sweet Potato + Butter','calories':int(calorie_target*0.28),'icon':'🐟'},
            'snacks':    {'name':'Peanut Butter + Banana + Protein Shake','calories':int(calorie_target*0.12),'icon':'🥤'},
        },
        'maintain': {
            'breakfast': {'name':'Oatmeal + Banana + Scrambled Eggs','calories':int(calorie_target*0.23),'icon':'🥣'},
            'lunch':     {'name':'Grilled Chicken + Brown Rice + Steamed Vegetables','calories':int(calorie_target*0.35),'icon':'🍗'},
            'dinner':    {'name':'Lentil Soup + Whole Grain Bread + Side Salad','calories':int(calorie_target*0.27),'icon':'🥗'},
            'snacks':    {'name':'Mixed Nuts + Low-fat Yogurt + Seasonal Fruit','calories':int(calorie_target*0.15),'icon':'🍎'},
        },
    }
    meals = mp.get(goal, mp['maintain'])

    # --- Macros ---
    if goal == 'weight_loss':
        p_pct, c_pct, f_pct = 0.35, 0.40, 0.25
    elif goal == 'weight_gain':
        p_pct, c_pct, f_pct = 0.30, 0.50, 0.20
    else:
        p_pct, c_pct, f_pct = 0.30, 0.45, 0.25
    macros = {
        'protein': int(calorie_target * p_pct / 4),
        'carbs':   int(calorie_target * c_pct / 4),
        'fats':    int(calorie_target * f_pct / 9),
        'fiber':   30 if goal == 'weight_gain' else 25,
    }

    # --- Insights from real data ---
    insights = []
    water_goal = float(profile.get('water_goal') or 2.0) if profile else 2.0

    water_row = execute_query("SELECT AVG(water_intake) FROM DAILY_LOG WHERE user_id=%(u)s AND log_date>=CURRENT_DATE-INTERVAL '7 days'", {'u': user_id})
    if water_row and water_row[0][0]:
        avg_w = float(water_row[0][0])
        if avg_w >= water_goal * 0.9:
            insights.append({'type':'success','icon':'💧','title':'Hydration On Track','text':f'You\'re averaging {avg_w:.1f}L/day — meeting your {water_goal}L goal. Excellent consistency!'})
        else:
            insights.append({'type':'warning','icon':'💧','title':'Hydration Alert','text':f'Avg water intake is {avg_w:.1f}L vs your {water_goal}L goal. Try drinking a glass every 2 hours.'})
    else:
        insights.append({'type':'info','icon':'💧','title':'Hydration Tip','text':f'Aim for {water_goal}L of water daily. Start each morning with a full glass before breakfast.'})

    cal_row = execute_query("SELECT AVG(total_calories_consumed) FROM DAILY_LOG WHERE user_id=%(u)s AND log_date>=CURRENT_DATE-INTERVAL '7 days' AND total_calories_consumed>0", {'u': user_id})
    if cal_row and cal_row[0][0]:
        avg_c = float(cal_row[0][0]); diff = avg_c - calorie_target
        if abs(diff) < 150:
            insights.append({'type':'success','icon':'🔥','title':'Calorie Balance','text':f'Your avg intake ({avg_c:.0f} kcal) is right on target ({calorie_target} kcal). Keep it consistent!'})
        elif diff > 150:
            insights.append({'type':'warning','icon':'🔥','title':'Calorie Surplus','text':f'You\'re averaging {diff:.0f} kcal above target. Try reducing portion sizes or adding a daily 20-min walk.'})
        else:
            insights.append({'type':'info','icon':'🔥','title':'Calorie Deficit','text':f'Eating {abs(diff):.0f} kcal below target. Ensure you\'re getting adequate nutrition — don\'t skip meals!'})

    sleep_row = execute_query("SELECT AVG(sleep_hours) FROM DAILY_LOG WHERE user_id=%(u)s AND log_date>=CURRENT_DATE-INTERVAL '7 days' AND sleep_hours>0", {'u': user_id})
    if sleep_row and sleep_row[0][0]:
        avg_s = float(sleep_row[0][0])
        if avg_s >= 7:
            insights.append({'type':'success','icon':'😴','title':'Sleep Quality','text':f'Averaging {avg_s:.1f} hrs sleep — excellent! Good sleep supports metabolism and recovery.'})
        else:
            insights.append({'type':'warning','icon':'😴','title':'Sleep Alert','text':f'Only {avg_s:.1f} hrs avg sleep. Poor sleep raises hunger hormones by 15%. Aim for 7-8 hours nightly.'})

    protein_tips = {
        'weight_loss':'High protein preserves muscle while losing fat. Include eggs, chicken, or lentils in every meal.',
        'weight_gain':'Protein is essential for muscle growth. Hit your daily target consistently — spread it across all meals.',
        'maintain':'Balanced protein supports energy and muscle throughout the day. Mix animal and plant sources.',
    }
    insights.append({'type':'info','icon':'💪','title':'Protein Strategy','text':protein_tips.get(goal, protein_tips['maintain'])})

    # --- Weekly plan ---
    weekly_themes = {
        'weight_loss': [
            ('Mon','High Protein Day','Lean meats + Vegetables'),
            ('Tue','Low Carb Day','Eggs + Fish + Leafy Greens'),
            ('Wed','Balanced Day','Balanced macros across all meals'),
            ('Thu','Detox Day','Fruits + Vegetables + Soup'),
            ('Fri','High Protein Day','Chicken + Lentils + Salad'),
            ('Sat','Flex Day','Moderate treat allowed'),
            ('Sun','Recovery Day','Light meals + Rest'),
        ],
        'weight_gain': [
            ('Mon','Muscle Building','High protein + Complex carbs'),
            ('Tue','Carb Loading','Rice + Pasta + Fruit'),
            ('Wed','Protein Day','Beef + Eggs + Dairy'),
            ('Thu','Mass Day','High calories + Protein shake'),
            ('Fri','Power Day','Pre/post workout nutrition'),
            ('Sat','Cheat Day','Enjoy favorite foods'),
            ('Sun','Recovery Day','Light proteins + Vegetables'),
        ],
        'maintain': [
            ('Mon','Balanced Start','Balanced macros all day'),
            ('Tue','High Protein','Chicken + Quinoa + Salad'),
            ('Wed','Mediterranean','Fish + Olive oil + Vegetables'),
            ('Thu','Plant-Based','Lentils + Beans + Whole Grains'),
            ('Fri','Energy Day','Complex carbs + Proteins'),
            ('Sat','Flex Day','Moderate treats allowed'),
            ('Sun','Light Day','Soups + Salads + Fruits'),
        ],
    }
    cal_offsets = {'weight_loss':[0,-0.05,0,-0.10,0,0.10,-0.05], 'weight_gain':[0,0.05,0,0.10,0,0.15,-0.10], 'maintain':[0,0,0,0,0,0.10,-0.10]}
    offsets = cal_offsets.get(goal, cal_offsets['maintain'])
    weekly = [{'day':d,'theme':t,'focus':f,'cal':int(calorie_target*(1+offsets[i]))} for i,(d,t,f) in enumerate(weekly_themes.get(goal, weekly_themes['maintain']))]

    # Confidence score
    confidence = 70
    if water_row and water_row[0][0]: confidence += 8
    if cal_row and cal_row[0][0]: confidence += 12
    if sleep_row and sleep_row[0][0]: confidence += 5
    confidence = min(confidence, 95)

    goal_display = {'weight_loss':'Lose Weight','weight_gain':'Build Muscle','maintain':'Maintain Fitness'}.get(goal,'Maintain Fitness')

    return {
        'goal': goal, 'goal_display': goal_display,
        'calorie_target': calorie_target,
        'bmi': bmi, 'bmi_category': bmi_category,
        'meals': meals, 'macros': macros,
        'insights': insights, 'weekly': weekly,
        'activity_level': (profile.get('activity_level') or 'Sedentary') if profile else 'Sedentary',
        'confidence': confidence,
    }


def get_user_profile(user_id):
    """
    Fetch the complete user profile as a dictionary for template access.
    Returns: Dictionary with user profile fields, or None if user not found
    """
    if not user_id:
        return None
    
    result = execute_query("""
        SELECT user_id, username, email, first_name, last_name, gender, 
               date_of_birth, height, weight, activity_level, sleep_hours, water_goal
        FROM USERS WHERE user_id = %(u)s
    """, {'u': user_id}, fetch=True)
    
    if result and result[0]:
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'height', 'weight', 'activity_level', 'sleep_hours', 'water_goal']
        row = result[0]
        return dict(zip(fields, row))
    return None


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
        check_query = "SELECT user_id FROM USERS WHERE username = %(username)s"
        existing_user = execute_query(check_query, {'username': username})
        
        if existing_user:
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        # Check if email already exists
        check_email = "SELECT user_id FROM USERS WHERE email = %(email)s"
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
                %(username)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s,
                %(dob)s::DATE, %(gender)s, %(weight)s, %(height)s,
                %(activity_level)s, %(dietary_preference)s, %(health_condition)s
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

    def safe_count(table):
        r = execute_query(f"SELECT COUNT(*) FROM {table}")
        return r[0][0] if r else 0

    total_users        = safe_count('USERS')
    total_goals        = safe_count('GOALS')
    total_meals        = safe_count('MEALS')
    total_activities   = safe_count('ACTIVITIES')
    total_logs         = safe_count('DAILY_LOG')
    total_meal_logs    = safe_count('MEAL_LOG')
    total_activity_logs= safe_count('ACTIVITY_LOG')
    total_mood_logs    = safe_count('MOOD_LOG')
    total_suggestions  = safe_count('SUGGESTIONS')
    total_reports      = safe_count('REPORTS')

    recent_users = execute_query("""
        SELECT user_id, username, first_name, last_name, email,
               TO_CHAR(created_at,'YYYY-MM-DD')
        FROM USERS ORDER BY user_id DESC LIMIT 5
    """)
    if recent_users is None:
        recent_users = execute_query("""
            SELECT user_id, username, first_name, last_name, email, 'N/A'
            FROM USERS ORDER BY user_id DESC LIMIT 5
        """) or []
    recent_users = recent_users or []

    return render_template('admin_dashboard.html',
                           total_users=total_users, total_goals=total_goals,
                           total_meals=total_meals, total_activities=total_activities,
                           total_logs=total_logs, total_meal_logs=total_meal_logs,
                           total_activity_logs=total_activity_logs,
                           total_mood_logs=total_mood_logs,
                           total_suggestions=total_suggestions,
                           total_reports=total_reports,
                           recent_users=recent_users)



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
    result = execute_query("SELECT COUNT(*) FROM DAILY_LOG WHERE user_id = %(user_id)s", {'user_id': user_id})
    if result:
        stats['total_logs'] = result[0][0]

    # Count meal logs (through DAILY_LOG since MEAL_LOG has no user_id)
    result = execute_query("""
        SELECT COUNT(*) FROM MEAL_LOG ml
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
    """, {'user_id': user_id})
    if result:
        stats['total_meals'] = result[0][0]

    # Count activity logs
    result = execute_query("""
        SELECT COUNT(*) FROM ACTIVITY_LOG al
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
    """, {'user_id': user_id})
    if result:
        stats['total_activities'] = result[0][0]

    # Count active goals
    result = execute_query("SELECT COUNT(*) FROM GOALS WHERE user_id = %(user_id)s AND status = 'Active'", {'user_id': user_id})
    if result:
        stats['active_goals'] = result[0][0]

    # Get today's daily log data
    today_log_q = execute_query("""
        SELECT dl.water_intake, dl.total_calories_consumed, dl.total_calories_burned,
               COALESCE(SUM(ml.total_calories), 0) as meal_cals,
               COALESCE(SUM(m.protein * ml.quantity), 0) as protein,
               COALESCE(SUM(m.carbohydrates * ml.quantity), 0) as carbs,
               COALESCE(SUM(m.fats * ml.quantity), 0) as fats,
               COALESCE(SUM(m.fiber * ml.quantity), 0) as fiber
        FROM DAILY_LOG dl
        LEFT JOIN MEAL_LOG ml ON ml.daily_log_id = dl.daily_log_id
        LEFT JOIN MEALS m ON ml.meal_id = m.meal_id
        WHERE dl.user_id = %(u)s AND DATE(dl.log_date) = CURRENT_DATE
        GROUP BY dl.daily_log_id, dl.water_intake, dl.total_calories_consumed, dl.total_calories_burned
    """, {'u': user_id})

    if today_log_q and today_log_q[0]:
        row = today_log_q[0]
        today_tracking = {
            'water': float(row[0] or 0),
            'calories': float(row[3] or 0),
            'calories_consumed': float(row[1] or 0),
            'calories_burned': float(row[2] or 0),
            'cal_burned': float(row[2] or 0),
            'protein': float(row[4] or 0),
            'carbs': float(row[5] or 0),
            'fats': float(row[6] or 0),
            'fiber': float(row[7] or 0),
            'steps': 0
        }
    else:
        today_tracking = {'water': 0, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed': 0, 'calories_burned': 0}

    # Get user profile (only columns that exist in USERS table)
    user_prof = execute_query("""
        SELECT user_id, username, email, first_name, last_name,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob, gender, weight, height,
               activity_level, dietary_preference, health_condition,
               TO_CHAR(created_date, 'YYYY-MM-DD') as created
        FROM USERS WHERE user_id = %(u)s
    """, {'u': user_id})
    user_profile = user_prof[0] if user_prof else []

    # Get active goal
    active_goal = execute_query("""
        SELECT goal_type, target_value FROM GOALS
        WHERE user_id = %(u)s AND status = 'Active'
        ORDER BY created_date DESC LIMIT 1
    """, {'u': user_id})

    # Compute health_metrics from user profile
    health_metrics = {}
    if user_profile and user_profile[7] and user_profile[8]:
        weight = float(user_profile[7])
        height_cm = float(user_profile[8])
        height_m = height_cm / 100.0
        bmi = weight / (height_m * height_m) if height_m > 0 else 0

        # BMI status
        if bmi < 18.5:
            bmi_status, bmi_color = 'Underweight', 'yellow'
        elif bmi < 25:
            bmi_status, bmi_color = 'Normal', 'green'
        elif bmi < 30:
            bmi_status, bmi_color = 'Overweight', 'yellow'
        else:
            bmi_status, bmi_color = 'Obese', 'red'

        # Estimate daily calories using Mifflin-St Jeor
        activity_level = user_profile[9] or 'Moderate'
        activity_multipliers = {
            'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55,
            'Active': 1.725, 'Very Active': 1.9
        }
        multiplier = activity_multipliers.get(activity_level, 1.55)

        # Estimate age from DOB
        age = 25  # default
        if user_profile[5]:
            try:
                dob = datetime.strptime(user_profile[5], '%Y-%m-%d')
                age = (datetime.now() - dob).days // 365
            except:
                pass

        gender = user_profile[6] or 'Male'
        if gender == 'Male':
            bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161

        daily_calories = int(bmr * multiplier)

        # Macro targets (approximate)
        protein_target = int(weight * 1.6)  # 1.6g per kg
        carbs_target = int(daily_calories * 0.45 / 4)  # 45% from carbs
        fats_target = int(daily_calories * 0.25 / 9)  # 25% from fats

        # Get target weight from active goal
        target_weight = float(active_goal[0][1]) if active_goal and active_goal[0][1] else None

        health_metrics = {
            'bmi': round(bmi, 1),
            'bmi_status': bmi_status,
            'bmi_color': bmi_color,
            'weight': weight,
            'target_weight': target_weight,
            'daily_calories': daily_calories,
            'protein': protein_target,
            'carbs': carbs_target,
            'fats': fats_target
        }

    # Add goal type to user_profile as index 16 (template expects it)
    # Template uses user_profile[16] for "Current Goal"
    # We build a list so the template indices work
    profile_list = list(user_profile) if user_profile else []
    # Pad to index 16: existing has indices 0-12 (13 items)
    while len(profile_list) < 16:
        profile_list.append(None)
    # Index 16 = goal type
    profile_list.append(active_goal[0][0] if active_goal else None)

    # Fetch today's meals grouped by category for the Meal Plan section
    today_meals_raw = execute_query("""
        SELECT m.meal_name, m.description, m.calories * ml.quantity,
               m.protein * ml.quantity, m.carbohydrates * ml.quantity,
               m.fats * ml.quantity, LOWER(COALESCE(m.meal_category, 'snack'))
        FROM MEAL_LOG ml
        JOIN MEALS m ON ml.meal_id = m.meal_id
        JOIN DAILY_LOG dl ON ml.daily_log_id = dl.daily_log_id
        WHERE dl.user_id = %(u)s AND DATE(dl.log_date) = CURRENT_DATE
        ORDER BY ml.meal_time
    """, {'u': user_id})

    today_meals = {'breakfast': [], 'lunch': [], 'dinner': [], 'snacks': []}
    if today_meals_raw:
        for row in today_meals_raw:
            cat = (row[6] or 'snack').lower()
            if 'breakfast' in cat:
                key = 'breakfast'
            elif 'lunch' in cat:
                key = 'lunch'
            elif 'dinner' in cat:
                key = 'dinner'
            else:
                key = 'snacks'
            today_meals[key].append({
                'name': row[0] or 'Unknown',
                'description': row[1] or '',
                'calories': round(float(row[2] or 0), 1),
                'protein': round(float(row[3] or 0), 1),
                'carbs': round(float(row[4] or 0), 1),
                'fats': round(float(row[5] or 0), 1),
            })

    profile = get_user_profile(user_id)
    return render_template('user_dashboard.html', stats=stats, today_tracking=today_tracking,
                           user_profile=profile_list, health_metrics=health_metrics,
                           profile=profile, today_meals=today_meals)

@app.route('/user/profile')
def user_profile():
    """User view own profile"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    result = execute_query("""
        SELECT user_id, username, email, first_name, last_name,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob,
               gender, weight, height, activity_level,
               dietary_preference, health_condition,
               TO_CHAR(created_date, 'YYYY-MM-DD') as created
        FROM USERS
        WHERE user_id = %(user_id)s
    """, {'user_id': user_id})

    if not result:
        profile = get_user_profile(user_id)
        return render_template('user_dashboard.html', view='profile', profile=profile)

    row = result[0]
    profile = {
        'user_id': row[0], 'username': row[1], 'email': row[2],
        'first_name': row[3], 'last_name': row[4], 'dob': row[5],
        'gender': row[6], 'weight': row[7], 'height': row[8],
        'activity_level': row[9], 'dietary_preference': row[10],
        'health_condition': row[11], 'created': row[12]
    }

    # Compute BMI
    if profile['weight'] and profile['height']:
        w = float(profile['weight'])
        h = float(profile['height']) / 100.0
        profile['bmi'] = round(w / (h * h), 1) if h > 0 else None
    else:
        profile['bmi'] = None

    # Compute daily calorie goal
    health_metrics = {}
    if profile['weight'] and profile['height']:
        w = float(profile['weight'])
        h_cm = float(profile['height'])
        age = 25
        if profile['dob']:
            try:
                dob = datetime.strptime(profile['dob'], '%Y-%m-%d')
                age = (datetime.now() - dob).days // 365
            except:
                pass
        multiplier = {'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55,
                      'Active': 1.725, 'Very Active': 1.9}.get(profile['activity_level'] or 'Moderate', 1.55)
        if profile['gender'] == 'Male':
            bmr = 10 * w + 6.25 * h_cm - 5 * age + 5
        else:
            bmr = 10 * w + 6.25 * h_cm - 5 * age - 161
        health_metrics['daily_calories'] = int(bmr * multiplier)

    # Get active goal
    goal_result = execute_query("""
        SELECT goal_type, target_value FROM GOALS
        WHERE user_id = %(u)s AND status = 'Active'
        ORDER BY created_date DESC LIMIT 1
    """, {'u': user_id})
    if goal_result:
        profile['goal_type'] = goal_result[0][0]
        profile['target_weight'] = goal_result[0][1]
    else:
        profile['goal_type'] = None
        profile['target_weight'] = None

    return render_template('user_dashboard.html', view='profile', profile=profile, health_metrics=health_metrics)


@app.route('/user/update-goal-status/<int:goal_id>', methods=['POST'])
def update_user_goal_status(goal_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    execute_query("UPDATE GOALS SET status = 'Completed' WHERE goal_id = %(g)s AND user_id = %(u)s", {'g': goal_id, 'u': session['user_id']}, fetch=False)
    flash('Goal marked as completed!', 'success')
    return redirect(url_for('user_goals'))

@app.route('/user/diet')
def user_diet():
    return redirect(url_for('ai_recommendation'))

@app.route('/user/add-update-goal', methods=['POST'])
def user_add_update_goal():
    """Redirect to add-goal for goal creation/update"""
    return redirect(url_for('user_add_goal'))

@app.route('/user/goals')
def user_goals():
    """User view own goals"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Get goals as rich dicts
    rows = execute_query("""
        SELECT goal_id, goal_type, target_value, current_value, status,
               TO_CHAR(start_date, 'YYYY-MM-DD') as start_date,
               TO_CHAR(target_date, 'YYYY-MM-DD') as target_date,
               start_date as start_raw, target_date as target_raw
        FROM GOALS
        WHERE user_id = %(user_id)s
        ORDER BY created_date DESC
    """, {'user_id': user_id})

    goals = []
    today = date.today()
    for r in (rows or []):
        g = {
            'goal_id': r[0], 'goal_type': r[1],
            'target_value': float(r[2]) if r[2] else 0,
            'current_value': float(r[3]) if r[3] else 0,
            'status': r[4], 'start_date': r[5], 'target_date': r[6],
        }
        start_raw = r[7]
        target_raw = r[8]

        # Compute progress correctly
        sv = g['current_value']
        tv = g['target_value']
        # For weight loss: progress = how much lost / how much need to lose
        # current_value is the starting weight set at goal creation
        # We need actual current weight from user profile or latest daily log
        g['progress'] = 0
        g['remaining'] = abs(sv - tv)
        g['direction'] = 'lose' if sv > tv else ('gain' if sv < tv else 'maintain')

        # Time calculations
        g['days_remaining'] = 0
        g['days_total'] = 0
        g['time_progress'] = 0
        if target_raw and start_raw:
            total_days = (target_raw - start_raw).days
            remaining_days = (target_raw - today).days
            g['days_total'] = max(total_days, 1)
            g['days_remaining'] = max(remaining_days, 0)
            g['time_progress'] = min(100, int(((total_days - remaining_days) / max(total_days, 1)) * 100))
            g['weeks_remaining'] = round(max(remaining_days, 0) / 7, 1)
        goals.append(g)

    # Get full user profile for template
    profile_res = execute_query("""
        SELECT user_id, username, email, first_name, last_name, gender, 
               date_of_birth, height, weight, activity_level, sleep_hours, water_goal
        FROM USERS WHERE user_id = %(u)s
    """, {'u': user_id})
    profile = profile_res[0] if profile_res else None

    # Get user profile for calorie calculation
    user_row = execute_query("""
        SELECT weight, height, gender, activity_level,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob
        FROM USERS WHERE user_id = %(u)s
    """, {'u': user_id})

    daily_calories = 2000
    current_weight = 0
    if user_row and user_row[0]:
        ur = user_row[0]
        current_weight = float(ur[0]) if ur[0] else 0
        if ur[0] and ur[1]:
            w = float(ur[0])
            h_cm = float(ur[1])
            age = 25
            if ur[4]:
                try:
                    dob = datetime.strptime(ur[4], '%Y-%m-%d')
                    age = (datetime.now() - dob).days // 365
                except:
                    pass
            mult = {'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55,
                    'Active': 1.725, 'Very Active': 1.9}.get(ur[3] or 'Moderate', 1.55)
            bmr = (10 * w + 6.25 * h_cm - 5 * age + 5) if ur[2] == 'Male' else (10 * w + 6.25 * h_cm - 5 * age - 161)
            daily_calories = int(bmr * mult)

    # Update goals with actual current weight and proper progress
    for g in goals:
        if g['status'] == 'Active':
            g['actual_weight'] = current_weight
            start_w = g['current_value']  # weight at goal creation
            target_w = g['target_value']
            diff_total = abs(start_w - target_w)
            if diff_total > 0:
                diff_done = abs(start_w - current_weight)
                # Only count progress in the right direction
                if g['direction'] == 'lose' and current_weight < start_w:
                    g['progress'] = min(100, int((diff_done / diff_total) * 100))
                elif g['direction'] == 'gain' and current_weight > start_w:
                    g['progress'] = min(100, int((diff_done / diff_total) * 100))
                elif g['direction'] == 'maintain':
                    g['progress'] = 100 if abs(current_weight - target_w) < 2 else 50
                else:
                    g['progress'] = 0
            g['remaining'] = round(abs(current_weight - target_w), 1)
            # Weekly target
            if g.get('weeks_remaining', 0) > 0:
                g['weekly_target'] = round(g['remaining'] / g['weeks_remaining'], 2)
            else:
                g['weekly_target'] = 0

    # Auto-complete goals where progress has reached 100%
    for g in goals:
        if g['status'] == 'Active' and g.get('progress', 0) >= 100:
            execute_query(
                "UPDATE GOALS SET status = 'Completed' WHERE goal_id = %(gid)s AND user_id = %(u)s",
                {'gid': g['goal_id'], 'u': user_id}, fetch=False
            )
            g['status'] = 'Completed'

    active_goals = [g for g in goals if g['status'] == 'Active']
    history_goals = [g for g in goals if g['status'] != 'Active']

    # Weight history from daily logs (last 10 entries with weight)
    weight_history = execute_query("""
        SELECT TO_CHAR(log_date, 'Mon DD') as dt, weight
        FROM DAILY_LOG
        WHERE user_id = %(u)s AND weight IS NOT NULL
        ORDER BY log_date DESC LIMIT 10
    """, {'u': user_id})
    weight_history = list(reversed(weight_history)) if weight_history else []

    # Ensure profile is fetched for template
    if not profile:
        profile = get_user_profile(user_id)
    return render_template('user_dashboard.html', view='goals', goals=goals,
                           active_goals=active_goals, history_goals=history_goals,
                           daily_calories=daily_calories, current_weight=current_weight,
                           weight_history=weight_history, profile=profile, user_profile=profile)


@app.route('/user/add-goal', methods=['GET', 'POST'])
def user_add_goal():
    """User add new or update goal"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # get existing active goal
    existing = execute_query("SELECT goal_id, goal_type, target_value, current_value, TO_CHAR(target_date, 'YYYY-MM-DD') FROM GOALS WHERE user_id = %(u)s AND status = 'Active' LIMIT 1", {'u': user_id}, fetch=True)
    existing_goal = existing[0] if existing else None

    if request.method == 'POST':
        goal_type = request.form.get('goal_type')
        target_value = request.form.get('target_value')
        current_value = request.form.get('current_value')
        target_date = request.form.get('target_date')
        goal_speed = request.form.get('goal_speed', 'Moderate')

        # Translate Fitness to valid DB value
        if goal_type == 'Muscle Building':
            goal_type = 'Muscle Gain'

        # Basic validation
        if not goal_type or not target_value or not target_date:
            flash('Please fill in all required fields.', 'error')
        else:
            if existing_goal:
                # Try with goal_speed column; fall back without it if column doesn't exist
                try:
                    query = """
                        UPDATE GOALS
                        SET goal_type = %(goal_type)s, target_value = %(target_value)s,
                            current_value = %(current_value)s, target_date = %(target_date)s::DATE,
                            goal_speed = %(goal_speed)s
                        WHERE goal_id = %(goal_id)s
                    """
                    execute_query(query, {
                        'goal_id': existing_goal[0], 'goal_type': goal_type,
                        'target_value': target_value, 'current_value': current_value,
                        'target_date': target_date, 'goal_speed': goal_speed
                    }, fetch=False)
                except Exception:
                    execute_query("""
                        UPDATE GOALS
                        SET goal_type = %(goal_type)s, target_value = %(target_value)s,
                            current_value = %(current_value)s, target_date = %(target_date)s::DATE
                        WHERE goal_id = %(goal_id)s
                    """, {
                        'goal_id': existing_goal[0], 'goal_type': goal_type,
                        'target_value': target_value, 'current_value': current_value,
                        'target_date': target_date
                    }, fetch=False)
                flash('Goal updated successfully!', 'success')
                return redirect(url_for('user_goals'))
            else:
                try:
                    query = """
                        INSERT INTO GOALS (user_id, goal_type, target_value, current_value,
                                          target_date, start_date, status, goal_speed)
                        VALUES (%(user_id)s, %(goal_type)s, %(target_value)s, %(current_value)s,
                                %(target_date)s::DATE, CURRENT_DATE, 'Active', %(goal_speed)s)
                    """
                    execute_query(query, {
                        'user_id': user_id, 'goal_type': goal_type,
                        'target_value': target_value, 'current_value': current_value,
                        'target_date': target_date, 'goal_speed': goal_speed
                    }, fetch=False)
                except Exception:
                    execute_query("""
                        INSERT INTO GOALS (user_id, goal_type, target_value, current_value,
                                          target_date, start_date, status)
                        VALUES (%(user_id)s, %(goal_type)s, %(target_value)s, %(current_value)s,
                                %(target_date)s::DATE, CURRENT_DATE, 'Active')
                    """, {
                        'user_id': user_id, 'goal_type': goal_type,
                        'target_value': target_value, 'current_value': current_value,
                        'target_date': target_date
                    }, fetch=False)
                flash('Goal created successfully!', 'success')
                return redirect(url_for('user_goals'))

    # Fetch profile for weight auto-fill and calorie calculation
    profile = get_user_profile(user_id)
    current_weight = float(profile['weight']) if profile and profile.get('weight') else 0.0

    # Compute maintenance calories for the smart panel
    if profile:
        w = float(profile.get('weight') or 0)
        h = float(profile.get('height') or 0)
        gender = profile.get('gender', 'Male')
        activity = profile.get('activity_level', 'Moderate')
        dob = profile.get('date_of_birth')
        age = 25
        if dob:
            try:
                dob_dt = datetime.strptime(str(dob), '%Y-%m-%d') if isinstance(dob, str) else dob
                age = (datetime.now() - dob_dt).days // 365
            except Exception:
                pass
        mult = {'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55,
                'Active': 1.725, 'Very Active': 1.9}.get(activity, 1.55)
        if w and h:
            bmr = (10 * w + 6.25 * h - 5 * age + 5) if gender == 'Male' else (10 * w + 6.25 * h - 5 * age - 161)
            maintenance_calories = int(bmr * mult)
        else:
            maintenance_calories = 2000
    else:
        maintenance_calories = 2000

    return render_template('user_dashboard.html', view='add_goal',
                           current_weight=current_weight,
                           existing_goal=existing_goal,
                           profile=profile,
                           maintenance_calories=maintenance_calories)


@app.route('/user/add-daily-log', methods=['GET', 'POST'])
def user_add_daily_log():
    """User add daily log - smart tracker"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        log_date = request.form.get('log_date', date.today().strftime('%Y-%m-%d'))
        water_intake = request.form.get('water_intake') or 0
        sleep_hours  = request.form.get('sleep_hours') or None
        weight       = request.form.get('weight') or None
        notes        = request.form.get('notes', '')

        existing = execute_query("""
            SELECT daily_log_id FROM DAILY_LOG
            WHERE user_id = %(user_id)s AND log_date = %(log_date)s::DATE
        """, {'user_id': user_id, 'log_date': log_date})

        if existing:
            execute_query("""
                UPDATE DAILY_LOG
                SET water_intake = %(water_intake)s,
                    sleep_hours  = %(sleep_hours)s,
                    weight       = %(weight)s,
                    notes        = %(notes)s
                WHERE user_id = %(user_id)s AND log_date = %(log_date)s::DATE
            """, {'user_id': user_id, 'log_date': log_date,
                  'water_intake': water_intake, 'sleep_hours': sleep_hours,
                  'weight': weight, 'notes': notes}, fetch=False)
        else:
            execute_query("""
                INSERT INTO DAILY_LOG (user_id, log_date, water_intake, sleep_hours, weight, notes)
                VALUES (%(user_id)s, %(log_date)s::DATE, %(water_intake)s, %(sleep_hours)s, %(weight)s, %(notes)s)
            """, {'user_id': user_id, 'log_date': log_date,
                  'water_intake': water_intake, 'sleep_hours': sleep_hours,
                  'weight': weight, 'notes': notes}, fetch=False)

        flash('Daily log saved!', 'success')
        return redirect(url_for('user_add_daily_log'))

    today = date.today().strftime('%Y-%m-%d')

    # Today's log entry
    today_log_result = execute_query("""
        SELECT daily_log_id, total_calories_consumed, total_calories_burned,
               water_intake, sleep_hours, weight, notes
        FROM DAILY_LOG
        WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
    """, {'user_id': user_id})

    today_log = None
    if today_log_result:
        r = today_log_result[0]
        today_log = {
            'daily_log_id': r[0],
            'water_intake':  float(r[3] or 0),
            'sleep_hours':   float(r[4]) if r[4] else None,
            'weight':        float(r[5]) if r[5] else None,
            'notes':         r[6] or ''
        }

    # Auto-calculated calories from meals
    meal_totals = execute_query("""
        SELECT COALESCE(SUM(ml.total_calories), 0),
               COALESCE(SUM(m.protein * ml.quantity), 0),
               COALESCE(SUM(m.carbohydrates * ml.quantity), 0),
               COALESCE(SUM(m.fats * ml.quantity), 0)
        FROM MEAL_LOG ml
        JOIN MEALS m ON ml.meal_id = m.meal_id
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
    """, {'user_id': user_id})

    today_consumed = today_protein = today_carbs = today_fats = 0.0
    if meal_totals and meal_totals[0]:
        today_consumed = float(meal_totals[0][0] or 0)
        today_protein  = float(meal_totals[0][1] or 0)
        today_carbs    = float(meal_totals[0][2] or 0)
        today_fats     = float(meal_totals[0][3] or 0)

    # Auto-calculated calories burned from activities
    burn_result = execute_query("""
        SELECT COALESCE(SUM(al.calories_burned), 0)
        FROM ACTIVITY_LOG al
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
    """, {'user_id': user_id})
    today_burned = float(burn_result[0][0] or 0) if burn_result else 0.0

    # Last recorded weight (previous day)
    last_w = execute_query("""
        SELECT weight, TO_CHAR(log_date, 'DD Mon') FROM DAILY_LOG
        WHERE user_id = %(user_id)s AND weight IS NOT NULL AND log_date < CURRENT_DATE
        ORDER BY log_date DESC FETCH FIRST 1 ROWS ONLY
    """, {'user_id': user_id})
    last_weight = float(last_w[0][0]) if last_w else None
    last_weight_date = last_w[0][1] if last_w else None

    # Calorie goal (default 2000)
    calorie_goal = 2000
    water_goal   = float(getattr(get_user_profile(user_id), '__class__', object) and 0) or 2.5
    profile = get_user_profile(user_id)
    if profile and profile.get('water_goal'):
        try:
            water_goal = float(profile['water_goal'])
        except (TypeError, ValueError):
            water_goal = 2.5

    # Recent logs
    logs = execute_query("""
        SELECT daily_log_id, TO_CHAR(log_date, 'DD Mon') as log_date,
               total_calories_consumed, total_calories_burned,
               water_intake, sleep_hours, weight
        FROM DAILY_LOG
        WHERE user_id = %(user_id)s
        ORDER BY log_date DESC FETCH FIRST 7 ROWS ONLY
    """, {'user_id': user_id})

    return render_template('user_dashboard.html',
        view='add_daily_log',
        daily_logs=logs,
        profile=profile,
        today_log=today_log,
        today_consumed=round(today_consumed, 1),
        today_burned=round(today_burned, 1),
        today_protein=round(today_protein, 1),
        today_carbs=round(today_carbs, 1),
        today_fats=round(today_fats, 1),
        calorie_goal=calorie_goal,
        water_goal=water_goal,
        last_weight=last_weight,
        last_weight_date=last_weight_date,
        today=today
    )


@app.route('/api/update-water', methods=['POST'])
def api_update_water():
    """AJAX: increment/reset water intake for today"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user_id = session['user_id']
    data   = request.get_json() or {}
    action = data.get('action', 'add')
    amount = float(data.get('amount', 0.25))

    row = execute_query("""
        SELECT daily_log_id, water_intake FROM DAILY_LOG
        WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
    """, {'user_id': user_id})

    if not row:
        new_water = amount if action == 'add' else 0.0
        execute_query("""
            INSERT INTO DAILY_LOG (user_id, log_date, water_intake)
            VALUES (%(user_id)s, CURRENT_DATE, %(w)s)
        """, {'user_id': user_id, 'w': new_water}, fetch=False)
    else:
        cur = float(row[0][1] or 0)
        if action == 'reset':
            new_water = 0.0
        else:
            new_water = max(0.0, cur + amount)
        execute_query("""
            UPDATE DAILY_LOG SET water_intake = %(w)s
            WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
        """, {'user_id': user_id, 'w': new_water}, fetch=False)

    return jsonify({'water': round(new_water, 2)})


@app.route('/api/meal-nutrition/<int:meal_id>')
def api_meal_nutrition(meal_id):
    """AJAX: return nutrition JSON for a single meal"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    result = execute_query("""
        SELECT meal_id, meal_name, meal_category, calories,
               protein, carbohydrates, fats, fiber, serving_size
        FROM MEALS WHERE meal_id = %(meal_id)s
    """, {'meal_id': meal_id})
    if result and result[0]:
        r = result[0]
        return jsonify({
            'meal_id':      r[0],
            'meal_name':    r[1],
            'category':     r[2],
            'calories':     float(r[3] or 0),
            'protein':      float(r[4] or 0),
            'carbs':        float(r[5] or 0),
            'fats':         float(r[6] or 0),
            'fiber':        float(r[7] or 0),
            'serving_size': r[8] or '1 serving'
        })
    return jsonify({'error': 'Not found'}), 404


@app.route('/api/add-custom-meal', methods=['POST'])
def api_add_custom_meal():
    """AJAX: add a brand-new meal to the global MEALS table"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data        = request.get_json() or {}
    meal_name   = (data.get('meal_name') or '').strip()
    category    = data.get('category', 'Snack')
    calories    = data.get('calories', 0)
    protein     = data.get('protein', 0)
    carbs       = data.get('carbohydrates', 0)
    fats        = data.get('fats', 0)
    fiber       = data.get('fiber', 0)
    serving     = (data.get('serving_size') or '1 serving').strip()
    description = (data.get('description') or '').strip()

    if not meal_name:
        return jsonify({'error': 'Meal name is required'}), 400

    valid_cats = {'Breakfast', 'Lunch', 'Dinner', 'Snack', 'Beverage'}
    if category not in valid_cats:
        category = 'Snack'

    try:
        # Try inserting; if duplicate, fall through to SELECT below
        execute_query("""
            INSERT INTO MEALS
                (meal_name, meal_category, calories, protein, carbohydrates,
                 fats, fiber, serving_size, description)
            VALUES (%(n)s, %(cat)s, %(cal)s, %(prot)s, %(carb)s,
                    %(fat)s, %(fib)s, %(srv)s, %(desc)s)
        """, {'n': meal_name, 'cat': category, 'cal': calories, 'prot': protein,
              'carb': carbs, 'fat': fats, 'fib': fiber,
              'srv': serving, 'desc': description}, fetch=False)
    except Exception:
        pass  # duplicate name — we'll return the existing row

    # Fetch the row (new or existing)
    row = execute_query("""
        SELECT meal_id, meal_name, meal_category, calories,
               protein, carbohydrates, fats, fiber, serving_size
        FROM MEALS WHERE meal_name = %(n)s
    """, {'n': meal_name})

    if row and row[0]:
        r = row[0]
        return jsonify({
            'success':      True,
            'meal_id':      r[0],
            'meal_name':    r[1],
            'category':     r[2] or 'Snack',
            'calories':     float(r[3] or 0),
            'protein':      float(r[4] or 0),
            'carbs':        float(r[5] or 0),
            'fats':         float(r[6] or 0),
            'fiber':        float(r[7] or 0),
            'serving_size': r[8] or '1 serving'
        })
    return jsonify({'error': 'Could not save meal'}), 500


@app.route('/api/add-custom-activity', methods=['POST'])
def api_add_custom_activity():
    """AJAX: add a brand-new activity to the global ACTIVITIES table"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data          = request.get_json() or {}
    activity_name = (data.get('activity_name') or '').strip()
    category      = data.get('category', 'Other')
    cpm           = data.get('calories_per_minute', 5)
    intensity     = data.get('intensity_level', 'Moderate')
    description   = (data.get('description') or '').strip()

    if not activity_name:
        return jsonify({'error': 'Activity name is required'}), 400

    valid_cats = {'Cardio', 'Strength', 'Flexibility', 'Sports', 'HIIT', 'Other'}
    if category not in valid_cats:
        category = 'Other'
    valid_int = {'Low', 'Moderate', 'High', 'Very High'}
    if intensity not in valid_int:
        intensity = 'Moderate'

    try:
        execute_query("""
            INSERT INTO ACTIVITIES
                (activity_name, activity_category, calories_per_minute,
                 intensity_level, description)
            VALUES (%(n)s, %(cat)s, %(cpm)s, %(int)s, %(desc)s)
        """, {'n': activity_name, 'cat': category, 'cpm': cpm,
              'int': intensity, 'desc': description}, fetch=False)
    except Exception:
        pass  # duplicate name — fall through

    row = execute_query("""
        SELECT activity_id, activity_name, activity_category,
               calories_per_minute, intensity_level, description
        FROM ACTIVITIES WHERE activity_name = %(n)s
    """, {'n': activity_name})

    if row and row[0]:
        r = row[0]
        return jsonify({
            'success':       True,
            'activity_id':   r[0],
            'activity_name': r[1],
            'category':      r[2] or 'Other',
            'cpm':           float(r[3] or 0),
            'intensity':     r[4] or 'Moderate',
            'description':   r[5] or ''
        })
    return jsonify({'error': 'Could not save activity'}), 500


@app.route('/user/add-meal-log', methods=['GET', 'POST'])
def user_add_meal_log():
    """User add meal log"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        meal_id   = request.form.get('meal_id')
        meal_time = request.form.get('meal_time')
        quantity  = request.form.get('quantity')

        if not meal_id or not meal_time or not quantity:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('user_add_meal_log'))

        if meal_time:
            meal_time = meal_time.replace('T', ' ')

        try:
            meal_result = execute_query(
                "SELECT calories FROM MEALS WHERE meal_id = %(meal_id)s",
                {'meal_id': meal_id})

            if not meal_result:
                flash('Selected meal not found', 'error')
                return redirect(url_for('user_add_meal_log'))

            total_calories = float(meal_result[0][0]) * float(quantity)

            today_log = execute_query("""
                SELECT daily_log_id FROM DAILY_LOG
                WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
            """, {'user_id': user_id})

            if not today_log:
                execute_query("""
                    INSERT INTO DAILY_LOG (user_id, log_date)
                    VALUES (%(user_id)s, CURRENT_DATE)
                """, {'user_id': user_id}, fetch=False)
                today_log = execute_query("""
                    SELECT daily_log_id FROM DAILY_LOG
                    WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
                """, {'user_id': user_id})

            daily_log_id = today_log[0][0] if today_log else None
            if not daily_log_id:
                flash('Failed to get daily log ID', 'error')
                return redirect(url_for('user_add_meal_log'))

            result = execute_query("""
                INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories)
                VALUES (%(daily_log_id)s, %(meal_id)s, %(meal_time)s::TIMESTAMP,
                        %(quantity)s, %(total_calories)s)
            """, {'daily_log_id': daily_log_id, 'meal_id': meal_id,
                  'meal_time': meal_time, 'quantity': quantity,
                  'total_calories': total_calories}, fetch=False)

            if result:
                flash('Meal logged successfully!', 'success')
            else:
                flash('Failed to add meal log', 'error')

        except ValueError as e:
            flash(f'Invalid number format: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error adding meal log: {str(e)}', 'error')

        return redirect(url_for('user_add_meal_log'))

    # GET - fetch all data
    meals = execute_query("""
        SELECT meal_id, meal_name, meal_category, calories,
               protein, carbohydrates, fats, fiber, serving_size, description
        FROM MEALS ORDER BY meal_category, meal_name
    """)

    today_log_row = execute_query("""
        SELECT daily_log_id FROM DAILY_LOG
        WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
    """, {'user_id': user_id})
    has_daily_log = bool(today_log_row)

    # Today's macro totals
    totals = execute_query("""
        SELECT COALESCE(SUM(ml.total_calories), 0),
               COALESCE(SUM(m.protein * ml.quantity), 0),
               COALESCE(SUM(m.carbohydrates * ml.quantity), 0),
               COALESCE(SUM(m.fats * ml.quantity), 0)
        FROM MEAL_LOG ml
        JOIN MEALS m ON ml.meal_id = m.meal_id
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
    """, {'user_id': user_id})

    today_consumed = today_protein = today_carbs = today_fats = 0.0
    if totals and totals[0]:
        today_consumed = float(totals[0][0] or 0)
        today_protein  = float(totals[0][1] or 0)
        today_carbs    = float(totals[0][2] or 0)
        today_fats     = float(totals[0][3] or 0)

    # Today's meal logs
    meal_logs = execute_query("""
        SELECT ml.meal_log_id, m.meal_name, m.meal_category,
               TO_CHAR(ml.meal_time, 'HH24:MI') as meal_time,
               ml.quantity, ml.total_calories
        FROM MEAL_LOG ml
        JOIN MEALS m ON ml.meal_id = m.meal_id
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
        ORDER BY ml.meal_time DESC
    """, {'user_id': user_id})

    profile = get_user_profile(user_id)
    return render_template('user_dashboard.html',
        view='add_meal_log',
        meals=meals,
        meal_logs=meal_logs,
        profile=profile,
        has_daily_log=has_daily_log,
        today_consumed=round(today_consumed, 1),
        today_protein=round(today_protein, 1),
        today_carbs=round(today_carbs, 1),
        today_fats=round(today_fats, 1),
        calorie_goal=2000
    )


@app.route('/user/add-activity-log', methods=['GET', 'POST'])
def user_add_activity_log():
    """User add activity log - smart tracker"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        activity_id   = request.form.get('activity_id')
        activity_time = request.form.get('activity_time')
        duration      = request.form.get('duration_minutes')
        notes         = request.form.get('notes', '')

        if not activity_id or not activity_time or not duration:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('user_add_activity_log'))

        if activity_time:
            activity_time = activity_time.replace('T', ' ')

        try:
            act_result = execute_query(
                "SELECT calories_per_minute FROM ACTIVITIES WHERE activity_id = %(activity_id)s",
                {'activity_id': activity_id})

            if not act_result:
                flash('Selected activity not found', 'error')
                return redirect(url_for('user_add_activity_log'))

            calories_per_minute = float(act_result[0][0] or 0)
            calories_burned     = round(calories_per_minute * float(duration), 2)

            today_log = execute_query("""
                SELECT daily_log_id FROM DAILY_LOG
                WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
            """, {'user_id': user_id})

            if not today_log:
                execute_query("""
                    INSERT INTO DAILY_LOG (user_id, log_date)
                    VALUES (%(user_id)s, CURRENT_DATE)
                """, {'user_id': user_id}, fetch=False)
                today_log = execute_query("""
                    SELECT daily_log_id FROM DAILY_LOG
                    WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
                """, {'user_id': user_id})

            daily_log_id = today_log[0][0] if today_log else None
            if not daily_log_id:
                flash('Failed to create daily log', 'error')
                return redirect(url_for('user_add_activity_log'))

            if execute_query("""
                INSERT INTO ACTIVITY_LOG
                    (daily_log_id, activity_id, activity_time, duration_minutes, calories_burned, notes)
                VALUES (%(daily_log_id)s, %(activity_id)s, %(activity_time)s::TIMESTAMP,
                        %(duration_minutes)s, %(calories_burned)s, %(notes)s)
            """, {'daily_log_id': daily_log_id, 'activity_id': activity_id,
                  'activity_time': activity_time, 'duration_minutes': duration,
                  'calories_burned': calories_burned, 'notes': notes}, fetch=False):
                flash(f'Activity logged! {calories_burned:.0f} kcal burned.', 'success')
            else:
                flash('Failed to add activity log', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('user_add_activity_log'))

    # --- GET ---
    activities = execute_query("""
        SELECT activity_id, activity_name, activity_category,
               calories_per_minute, intensity_level, description
        FROM ACTIVITIES ORDER BY activity_category, activity_name
    """)

    today_log_row = execute_query("""
        SELECT daily_log_id FROM DAILY_LOG
        WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
    """, {'user_id': user_id})
    has_daily_log = bool(today_log_row)

    # Today totals
    today_totals = execute_query("""
        SELECT COALESCE(SUM(al.calories_burned), 0),
               COALESCE(SUM(al.duration_minutes), 0)
        FROM ACTIVITY_LOG al
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
    """, {'user_id': user_id})
    today_burned  = float(today_totals[0][0] or 0) if today_totals else 0.0
    today_minutes = float(today_totals[0][1] or 0) if today_totals else 0.0

    # Weekly stats (last 7 days)
    weekly = execute_query("""
        SELECT COALESCE(SUM(al.calories_burned), 0),
               COALESCE(SUM(al.duration_minutes), 0),
               COUNT(al.activity_log_id)
        FROM ACTIVITY_LOG al
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
          AND d.log_date >= CURRENT_DATE - INTERVAL '7 days'
    """, {'user_id': user_id})
    weekly_burned   = float(weekly[0][0] or 0) if weekly else 0.0
    weekly_minutes  = float(weekly[0][1] or 0) if weekly else 0.0
    weekly_sessions = int(weekly[0][2] or 0) if weekly else 0

    # Today's activity log entries
    activity_logs = execute_query("""
        SELECT al.activity_log_id, a.activity_name, a.activity_category,
               TO_CHAR(al.activity_time, 'HH24:MI') as activity_time,
               al.duration_minutes, al.calories_burned, a.intensity_level
        FROM ACTIVITY_LOG al
        JOIN ACTIVITIES a ON al.activity_id = a.activity_id
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
        ORDER BY al.activity_time DESC
    """, {'user_id': user_id})

    profile = get_user_profile(user_id)
    return render_template('user_dashboard.html',
        view='add_activity_log',
        activities=activities,
        activity_logs=activity_logs,
        profile=profile,
        has_daily_log=has_daily_log,
        today_burned=round(today_burned, 1),
        today_minutes=round(today_minutes, 1),
        weekly_burned=round(weekly_burned, 1),
        weekly_minutes=round(weekly_minutes, 1),
        weekly_sessions=weekly_sessions
    )


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
        WHERE user_id = %(user_id)s
        ORDER BY created_date DESC
    """
    
    suggestions = execute_query(query, {'user_id': user_id})
    profile = get_user_profile(user_id)
    return render_template('user_dashboard.html', view='suggestions', suggestions=suggestions, profile=profile)


@app.route('/user/add-mood-log', methods=['GET', 'POST'])
def user_add_mood_log():
    """User add mood log — smart tracker with insights"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        mood_rating      = request.form.get('mood_rating')
        stress_level     = request.form.get('stress_level', 'Moderate')
        energy_level     = request.form.get('energy_level', 'Moderate')
        triggers         = request.form.getlist('triggers')
        notes_raw        = request.form.get('notes', '')

        # Validate DB constraints
        valid_levels = {'Low', 'Moderate', 'High'}
        if stress_level not in valid_levels:
            stress_level = 'Moderate'
        if energy_level not in valid_levels:
            energy_level = 'Moderate'

        # Append triggers to notes
        notes = notes_raw
        if triggers:
            trigger_str = 'Triggers: ' + ', '.join(triggers)
            notes = (notes + ' | ' + trigger_str).strip(' |') if notes else trigger_str

        today_log = execute_query("""
            SELECT daily_log_id FROM DAILY_LOG
            WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
        """, {'user_id': user_id})

        if not today_log:
            execute_query("""
                INSERT INTO DAILY_LOG (user_id, log_date)
                VALUES (%(user_id)s, CURRENT_DATE)
            """, {'user_id': user_id}, fetch=False)
            today_log = execute_query("""
                SELECT daily_log_id FROM DAILY_LOG
                WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
            """, {'user_id': user_id})

        daily_log_id = today_log[0][0] if today_log else None

        if daily_log_id:
            try:
                if execute_query("""
                    INSERT INTO MOOD_LOG
                        (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
                    VALUES (%(daily_log_id)s, %(mood_rating)s, %(stress_level)s,
                            %(energy_level)s, %(notes)s, CURRENT_TIMESTAMP)
                """, {'daily_log_id': daily_log_id, 'mood_rating': mood_rating,
                      'stress_level': stress_level, 'energy_level': energy_level,
                      'notes': notes}, fetch=False):
                    flash('Mood logged! Keep tracking your wellbeing.', 'success')
                else:
                    flash('Failed to add mood log', 'error')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        else:
            flash('Failed to create daily log', 'error')

        return redirect(url_for('user_add_mood_log'))

    # --- GET ---
    has_daily_log = bool(execute_query("""
        SELECT daily_log_id FROM DAILY_LOG
        WHERE user_id = %(user_id)s AND log_date = CURRENT_DATE
    """, {'user_id': user_id}))

    # Today's latest mood entry
    today_mood_row = execute_query("""
        SELECT m.mood_rating, m.stress_level, m.energy_level, m.notes,
               TO_CHAR(m.log_time, 'HH24:MI') as log_time
        FROM MOOD_LOG m
        JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s AND d.log_date = CURRENT_DATE
        ORDER BY m.log_time DESC FETCH FIRST 1 ROWS ONLY
    """, {'user_id': user_id})
    today_mood = None
    if today_mood_row:
        r = today_mood_row[0]
        today_mood = {'rating': r[0], 'stress': r[1], 'energy': r[2],
                      'notes': r[3] or '', 'time': r[4]}

    # Last 7 days trend (one entry per day — most recent for that day)
    weekly_trend = execute_query("""
        SELECT TO_CHAR(d.log_date, 'Dy') as day_name,
               TO_CHAR(d.log_date, 'DD Mon') as label,
               ROUND(AVG(m.mood_rating), 1) as avg_rating,
               MODE() WITHIN GROUP (ORDER BY m.energy_level) as energy,
               MODE() WITHIN GROUP (ORDER BY m.stress_level) as stress
        FROM DAILY_LOG d
        JOIN MOOD_LOG m ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
          AND d.log_date >= CURRENT_DATE - INTERVAL '6 days'
        GROUP BY d.log_date
        ORDER BY d.log_date ASC
    """, {'user_id': user_id})

    # Weekly average mood
    avg_result = execute_query("""
        SELECT ROUND(AVG(m.mood_rating), 1), COUNT(m.mood_log_id)
        FROM MOOD_LOG m
        JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
          AND d.log_date >= CURRENT_DATE - INTERVAL '6 days'
    """, {'user_id': user_id})
    avg_mood_week  = float(avg_result[0][0] or 0) if avg_result and avg_result[0][0] else None
    total_logs_week = int(avg_result[0][1] or 0) if avg_result else 0

    # Smart insights
    insights = []
    # Insight 1: mood on active days vs inactive days
    act_insight = execute_query("""
        SELECT
            ROUND(AVG(CASE WHEN act_count > 0 THEN avg_mood ELSE NULL END), 1),
            ROUND(AVG(CASE WHEN act_count = 0 THEN avg_mood ELSE NULL END), 1)
        FROM (
            SELECT d.daily_log_id,
                   AVG(m.mood_rating)            AS avg_mood,
                   COUNT(al.activity_log_id)     AS act_count
            FROM DAILY_LOG d
            LEFT JOIN MOOD_LOG m  ON m.daily_log_id  = d.daily_log_id
            LEFT JOIN ACTIVITY_LOG al ON al.daily_log_id = d.daily_log_id
            WHERE d.user_id = %(user_id)s
              AND d.log_date >= CURRENT_DATE - INTERVAL '30 days'
              AND m.mood_log_id IS NOT NULL
            GROUP BY d.daily_log_id
        ) sub
    """, {'user_id': user_id})
    if act_insight and act_insight[0][0] and act_insight[0][1]:
        with_act = float(act_insight[0][0])
        no_act   = float(act_insight[0][1])
        if with_act - no_act >= 0.3:
            insights.append({'icon': '💪', 'text': f'You feel better on days you exercise (avg {with_act}/5 vs {no_act}/5 without).'})

    # Insight 2: mood vs sleep quality
    sleep_insight = execute_query("""
        SELECT
            ROUND(AVG(CASE WHEN d.sleep_hours >= 7 THEN m.mood_rating ELSE NULL END), 1),
            ROUND(AVG(CASE WHEN d.sleep_hours < 7  AND d.sleep_hours > 0 THEN m.mood_rating ELSE NULL END), 1)
        FROM DAILY_LOG d
        JOIN MOOD_LOG m ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
          AND d.log_date >= CURRENT_DATE - INTERVAL '30 days'
          AND d.sleep_hours IS NOT NULL
    """, {'user_id': user_id})
    if sleep_insight and sleep_insight[0][0] and sleep_insight[0][1]:
        good_sleep = float(sleep_insight[0][0])
        bad_sleep  = float(sleep_insight[0][1])
        if good_sleep - bad_sleep >= 0.3:
            insights.append({'icon': '😴', 'text': f'Better sleep = better mood — avg {good_sleep}/5 on 7h+ vs {bad_sleep}/5 on less.'})

    # Insight 3: stress on days with meals vs without
    stress_insight = execute_query("""
        SELECT
            MODE() WITHIN GROUP (ORDER BY m.stress_level) as common_stress,
            COUNT(*) as cnt
        FROM MOOD_LOG m
        JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
          AND d.log_date >= CURRENT_DATE - INTERVAL '14 days'
    """, {'user_id': user_id})
    if stress_insight and stress_insight[0][0]:
        common_stress = stress_insight[0][0]
        if common_stress == 'High':
            insights.append({'icon': '🧘', 'text': 'High stress detected frequently. Consider adding short walks or breathing exercises.'})
        elif common_stress == 'Low':
            insights.append({'icon': '✨', 'text': 'Your stress levels have been consistently low — great work managing your wellbeing!'})

    # Recent mood logs
    mood_logs = execute_query("""
        SELECT m.mood_log_id,
               TO_CHAR(d.log_date, 'DD Mon') as log_date,
               TO_CHAR(m.log_time, 'HH24:MI') as log_time,
               m.mood_rating, m.stress_level, m.energy_level, m.notes
        FROM MOOD_LOG m
        JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
        ORDER BY m.log_time DESC
        FETCH FIRST 10 ROWS ONLY
    """, {'user_id': user_id})

    profile = get_user_profile(user_id)
    return render_template('user_dashboard.html',
        view='add_mood_log',
        mood_logs=mood_logs,
        profile=profile,
        has_daily_log=has_daily_log,
        today_mood=today_mood,
        weekly_trend=weekly_trend,
        avg_mood_week=avg_mood_week,
        total_logs_week=total_logs_week,
        insights=insights
    )


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
        WHERE user_id = %(user_id)s
        ORDER BY generated_date DESC
    """
    reports = execute_query(query, {'user_id': user_id})

    # Pull live summary stats from DAILY_LOG for the stats overview strip
    stats_query = """
        SELECT
            COUNT(*)                                          AS total_logs,
            ROUND(AVG(total_calories_consumed)::numeric, 0)  AS avg_cal_all,
            ROUND(AVG(CASE WHEN log_date >= CURRENT_DATE - INTERVAL '7 days'
                           THEN total_calories_consumed END)::numeric, 0) AS avg_cal_7d,
            ROUND(AVG(CASE WHEN log_date >= CURRENT_DATE - INTERVAL '30 days'
                           THEN total_calories_consumed END)::numeric, 0) AS avg_cal_30d,
            ROUND(AVG(CASE WHEN log_date >= CURRENT_DATE - INTERVAL '7 days'
                           THEN water_intake END)::numeric, 2)            AS avg_water_7d,
            ROUND(AVG(CASE WHEN log_date >= CURRENT_DATE - INTERVAL '7 days'
                           THEN sleep_hours END)::numeric, 1)             AS avg_sleep_7d,
            MAX(weight)                                       AS latest_weight,
            MIN(log_date)                                     AS first_log,
            MAX(log_date)                                     AS last_log,
            SUM(CASE WHEN log_date >= CURRENT_DATE - INTERVAL '7 days'
                     THEN total_calories_burned ELSE 0 END)   AS burned_7d
        FROM DAILY_LOG
        WHERE user_id = %(user_id)s
    """
    stats_row = execute_query(stats_query, {'user_id': user_id})
    log_stats = {}
    if stats_row:
        r = stats_row[0]
        log_stats = {
            'total_logs':    r[0] or 0,
            'avg_cal_all':   r[1] or 0,
            'avg_cal_7d':    r[2] or 0,
            'avg_cal_30d':   r[3] or 0,
            'avg_water_7d':  r[4] or 0,
            'avg_sleep_7d':  r[5] or 0,
            'latest_weight': r[6] or 0,
            'first_log':     str(r[7]) if r[7] else None,
            'last_log':      str(r[8]) if r[8] else None,
            'burned_7d':     r[9] or 0,
        }

    profile = get_user_profile(user_id)
    return render_template('user_dashboard.html', view='reports', reports=reports,
                           log_stats=log_stats, profile=profile)


# ============================================================================
# RUN APPLICATION
# ============================================================================


@app.route('/api/add-water-glass', methods=['POST'])
def api_add_water_glass():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    from datetime import date
    
    # Check if a daily log exists for today
    existing = execute_query("SELECT daily_log_id, water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': user_id})
    
    if existing:
        current_water = float(existing[0][1] or 0)
        new_water = round(current_water + 0.25, 2)  # 1 glass = 250ml = 0.25L
        execute_query("UPDATE DAILY_LOG SET water_intake = %(w)s WHERE daily_log_id = %(id)s", {'w': new_water, 'id': existing[0][0]}, fetch=False)
    else:
        new_water = 0.25
        execute_query("INSERT INTO DAILY_LOG (user_id, log_date, water_intake) VALUES (%(u)s, CURRENT_DATE, %(w)s)", {'u': user_id, 'w': new_water}, fetch=False)

    glasses = int(round(new_water / 0.25))
    return jsonify({'success': True, 'message': 'Water glass added successfully', 'water_glasses': glasses})

@app.route('/api/update-water-goal', methods=['POST'])
def api_update_water_goal():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
    # the frontend typically sends JSON, but let's be safe
    data = request.json or {}
    water_goal = data.get('water_goal', 8)
    session['water_goal'] = water_goal
    
    return jsonify({'success': True, 'message': 'Water goal updated!'})


@app.route('/api/update-profile', methods=['POST'])
def api_update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401

    user_id = session['user_id']
    data = request.json or {}
    fields = data.get('fields', {})

    if not fields:
        return jsonify({'success': False, 'error': 'No fields provided'}), 400

    # --- Input range validation ---
    CONTACT_ADMIN = ' For unusual values, please contact admin for support.'
    if 'weight' in fields:
        try:
            w = float(fields['weight'])
            if w < 20 or w > 300:
                return jsonify({'success': False, 'error': f'Weight must be between 20 and 300 kg.{CONTACT_ADMIN}'}), 400
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid weight value.'}), 400

    if 'height' in fields:
        try:
            h = float(fields['height'])
            if h < 50 or h > 250:
                return jsonify({'success': False, 'error': f'Height must be between 50 and 250 cm.{CONTACT_ADMIN}'}), 400
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid height value.'}), 400

    if 'date_of_birth' in fields:
        try:
            from datetime import date as _date
            dob = datetime.strptime(str(fields['date_of_birth']), '%Y-%m-%d').date()
            age_days = (_date.today() - dob).days
            if age_days < 365 * 10 or age_days > 365 * 120:
                return jsonify({'success': False, 'error': f'Age must be between 10 and 120 years.{CONTACT_ADMIN}'}), 400
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid date of birth format (use YYYY-MM-DD).'}), 400

    # Whitelist of allowed columns in USERS table
    allowed_columns = {
        'first_name', 'last_name', 'email', 'date_of_birth',
        'gender', 'weight', 'height', 'activity_level',
        'dietary_preference', 'health_condition'
    }

    # Build SET clause from provided fields
    set_parts = []
    params = {'user_id': user_id}
    for key, value in fields.items():
        if key in allowed_columns and value is not None:
            param_name = f'p_{key}'
            if key == 'date_of_birth':
                set_parts.append(f"{key} = %({param_name})s::DATE")
            elif key in ('weight', 'height'):
                set_parts.append(f"{key} = %({param_name})s::NUMERIC")
            else:
                set_parts.append(f"{key} = %({param_name})s")
            params[param_name] = value

    if not set_parts:
        return jsonify({'success': False, 'error': 'No valid fields to update'}), 400

    query = f"UPDATE USERS SET {', '.join(set_parts)} WHERE user_id = %(user_id)s"

    try:
        result = execute_query(query, params, fetch=False)
        if result:
            # Update session if name changed
            if 'first_name' in fields:
                session['first_name'] = fields['first_name']
            if 'last_name' in fields:
                session['last_name'] = fields['last_name']
            if 'email' in fields:
                session['email'] = fields['email']
            return jsonify({'success': True, 'message': 'Profile updated successfully!'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update profile'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# --- Recovered missing routes ---
@app.route('/user/user-add-water')
def user_add_water():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']

    # Get today's water intake
    today_log_q = execute_query("SELECT water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': user_id})
    today_water = float(today_log_q[0][0] or 0) if today_log_q and today_log_q[0][0] is not None else 0

    today_tracking = {'water': today_water}

    # Get user profile for water goal display
    user_prof = execute_query("""
        SELECT user_id, username, email, first_name, last_name,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD'), gender, weight, height,
               activity_level, dietary_preference, health_condition,
               TO_CHAR(created_date, 'YYYY-MM-DD')
        FROM USERS WHERE user_id = %(u)s
    """, {'u': user_id})
    user_profile = list(user_prof[0]) if user_prof else []
    profile = get_user_profile(user_id)

    return render_template('user_dashboard.html', view='add_water',
                           today_tracking=today_tracking, user_profile=user_profile, profile=profile)


@app.route('/user/ai-recommendation', methods=['GET', 'POST'])
def ai_recommendation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    profile = get_user_profile(user_id)

    # Map any of the 9 goal options to the 3 plan categories
    _goal_to_plan = {
        'lose_weight': 'weight_loss', 'weight_loss': 'weight_loss',
        'gain_weight': 'weight_gain', 'build_muscle': 'weight_gain',
        'weight_gain': 'weight_gain', 'increase_strength': 'weight_gain',
        'maintain_weight': 'maintain', 'maintain': 'maintain',
        'improve_fitness': 'maintain', 'improve_endurance': 'maintain',
        'healthy_lifestyle': 'maintain', 'medical_diet': 'maintain',
    }

    # Determine goal: POST selection > active DB goal > default
    if request.method == 'POST':
        selected_goal = request.form.get('goal', 'maintain_weight')
    else:
        active_goal_row = execute_query(
            "SELECT goal_type FROM GOALS WHERE user_id=%(u)s AND status='Active' ORDER BY created_date DESC LIMIT 1",
            {'u': user_id}
        )
        if active_goal_row:
            gt = (active_goal_row[0][0] or '').lower().replace(' ', '_')
            # Map DB goal_type string to dropdown value
            if 'lose' in gt or 'loss' in gt:
                selected_goal = 'lose_weight'
            elif 'gain_weight' in gt:
                selected_goal = 'gain_weight'
            elif 'build' in gt or 'muscle' in gt or 'bulk' in gt:
                selected_goal = 'build_muscle'
            elif 'maintain' in gt:
                selected_goal = 'maintain_weight'
            elif 'strength' in gt:
                selected_goal = 'increase_strength'
            elif 'endurance' in gt:
                selected_goal = 'improve_endurance'
            elif 'healthy' in gt or 'lifestyle' in gt:
                selected_goal = 'healthy_lifestyle'
            elif 'medical' in gt:
                selected_goal = 'medical_diet'
            else:
                selected_goal = 'improve_fitness'
        else:
            selected_goal = 'maintain_weight'

    plan_goal = _goal_to_plan.get(selected_goal, 'maintain')
    ai_plan = generate_ai_plan(profile, user_id, plan_goal)

    # Save snapshot to SUGGESTIONS table on every POST (explicit regenerate)
    if request.method == 'POST' and ai_plan:
        goal_labels = {
            'lose_weight': 'Lose Weight', 'gain_weight': 'Gain Weight',
            'build_muscle': 'Build Muscle', 'maintain_weight': 'Maintain Weight',
            'improve_fitness': 'Improve Fitness', 'increase_strength': 'Increase Strength',
            'improve_endurance': 'Improve Endurance', 'healthy_lifestyle': 'Healthy Lifestyle',
            'medical_diet': 'Medical Diet',
            # legacy keys
            'weight_loss': 'Lose Weight', 'weight_gain': 'Build Muscle', 'maintain': 'Maintain Weight',
        }
        summary = (
            f"Goal: {goal_labels.get(selected_goal,'Maintain')} | "
            f"Calories: {ai_plan['calorie_target']} kcal/day | "
            f"Protein: {ai_plan['macros']['protein']}g, Carbs: {ai_plan['macros']['carbs']}g, Fats: {ai_plan['macros']['fats']}g | "
            f"BMI: {ai_plan['bmi']} ({ai_plan['bmi_category']}) | Confidence: {ai_plan['confidence']}%"
        )
        reasoning = (
            f"Based on BMI {ai_plan['bmi']} ({ai_plan['bmi_category']}), "
            f"activity level {ai_plan['activity_level']}, and 7-day data analysis. "
            f"Target: {ai_plan['calorie_target']} kcal using Mifflin-St Jeor formula."
        )
        execute_query(
            """INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, reasoning_type)
               VALUES (%(u)s, 'Diet', %(st)s, %(r)s, %(rt)s)""",
            {'u': user_id, 'st': summary[:1000], 'r': reasoning[:1000], 'rt': selected_goal},
            fetch=False
        )

    return render_template('user_dashboard.html', view='ai_recommendation',
                           profile=profile, ai_plan=ai_plan, selected_goal=selected_goal)


@app.route('/user/ai-recommendation-history')
def ai_recommendation_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    profile = get_user_profile(user_id)
    history = execute_query(
        """SELECT suggestion_id, suggestion_text, reasoning, reasoning_type,
                  TO_CHAR(created_date, 'DD Mon YYYY') as created_date,
                  TO_CHAR(created_date, 'HH12:MI AM') as created_time
           FROM SUGGESTIONS
           WHERE user_id=%(u)s AND suggestion_type='Diet'
           ORDER BY created_date DESC
           LIMIT 20""",
        {'u': user_id}
    )
    return render_template('user_dashboard.html', view='ai_history',
                           profile=profile, history=history)

@app.route('/user/ml-recommendation')
def ml_recommendation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('ai_recommendation'))

@app.route('/user/user-progress')
def user_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']

    # Get today's tracking
    today_log_q = execute_query("""
        SELECT COALESCE(dl.total_calories_consumed, 0),
               COALESCE(SUM(m.protein * ml.quantity), 0),
               COALESCE(dl.water_intake, 0)
        FROM DAILY_LOG dl
        LEFT JOIN MEAL_LOG ml ON ml.daily_log_id = dl.daily_log_id
        LEFT JOIN MEALS m ON ml.meal_id = m.meal_id
        WHERE dl.user_id = %(u)s AND DATE(dl.log_date) = CURRENT_DATE
        GROUP BY dl.daily_log_id, dl.total_calories_consumed, dl.water_intake
    """, {'u': user_id})

    today_tracking = {'calories': 0, 'protein': 0, 'water_intake': 0}
    if today_log_q and today_log_q[0]:
        today_tracking = {
            'calories': float(today_log_q[0][0] or 0),
            'protein': float(today_log_q[0][1] or 0),
            'water_intake': float(today_log_q[0][2] or 0)
        }

    # Get last 7 days logs
    recent_logs = execute_query("""
        SELECT TO_CHAR(log_date, 'YYYY-MM-DD'), total_calories_consumed,
               total_calories_burned, water_intake, sleep_hours, weight
        FROM DAILY_LOG
        WHERE user_id = %(u)s
        ORDER BY log_date DESC
        LIMIT 7
    """, {'u': user_id})

    # Get active goal
    current_goal = execute_query("""
        SELECT goal_id, goal_type, target_value, current_value, status,
               TO_CHAR(start_date, 'YYYY-MM-DD'), TO_CHAR(target_date, 'YYYY-MM-DD')
        FROM GOALS
        WHERE user_id = %(u)s AND status = 'Active'
        ORDER BY created_date DESC LIMIT 1
    """, {'u': user_id})
    current_goal = current_goal[0] if current_goal else None

    # Get user profile for sleep hours display
    user_prof = execute_query("""
        SELECT user_id, username, email, first_name, last_name,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD'), gender, weight, height,
               activity_level, dietary_preference, health_condition,
               TO_CHAR(created_date, 'YYYY-MM-DD')
        FROM USERS WHERE user_id = %(u)s
    """, {'u': user_id})
    user_profile = list(user_prof[0]) if user_prof else []
    profile = get_user_profile(user_id)

    return render_template('user_dashboard.html', view='progress',
                           today_tracking=today_tracking, recent_logs=recent_logs,
                           current_goal=current_goal, user_profile=user_profile,
                           health_metrics={}, profile=profile)


@app.route('/user/help')
def user_help():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    profile = get_user_profile(session['user_id'])
    return render_template('user_dashboard.html', view='help', profile=profile)


# --- Dummy routes for missing endpoints ---

def _admin_required():
    return 'user_id' in session and session.get('is_admin')


@app.route('/admin_users')
def admin_users():
    if not _admin_required():
        return redirect(url_for('login'))
    search_name   = request.args.get('search_name', '')
    filter_gender = request.args.get('filter_gender', '')
    users = execute_query("""
        SELECT user_id, username, email, first_name, last_name, gender,
               date_of_birth, weight, activity_level,
               TO_CHAR(created_at,'YYYY-MM-DD')
        FROM USERS
        WHERE (%(s)s = '' OR username ILIKE %(sl)s
               OR first_name ILIKE %(sl)s OR last_name ILIKE %(sl)s)
          AND (%(g)s = '' OR gender = %(g)s)
        ORDER BY user_id DESC
    """, {'s': search_name, 'sl': f'%{search_name}%', 'g': filter_gender})
    if users is None:
        users = execute_query("""
            SELECT user_id, username, email, first_name, last_name, gender,
                   date_of_birth, weight, activity_level, 'N/A'
            FROM USERS
            WHERE (%(s)s = '' OR username ILIKE %(sl)s
                   OR first_name ILIKE %(sl)s OR last_name ILIKE %(sl)s)
              AND (%(g)s = '' OR gender = %(g)s)
            ORDER BY user_id DESC
        """, {'s': search_name, 'sl': f'%{search_name}%', 'g': filter_gender})
    users = users or []
    return render_template('admin_dashboard.html', view='users', users=users,
                           search_name=search_name, filter_gender=filter_gender)


@app.route('/admin_view_user/<int:user_id>')
def admin_view_user(user_id):
    if not _admin_required():
        return redirect(url_for('login'))
    user = execute_query("""
        SELECT user_id, username, email, first_name, last_name,
               date_of_birth, gender, weight, height, activity_level,
               0 AS is_admin, 'N/A' AS joined
        FROM USERS WHERE user_id = %(id)s
    """, {'id': user_id})
    user = user[0] if user else None
    goals = execute_query("""
        SELECT goal_id, goal_type, target_value, current_value,
               start_date, target_date, status
        FROM GOALS WHERE user_id = %(id)s ORDER BY goal_id DESC
    """, {'id': user_id}) or []
    logs = execute_query("""
        SELECT TO_CHAR(log_date,'YYYY-MM-DD'), total_calories_consumed,
               total_calories_burned, water_intake, weight
        FROM DAILY_LOG WHERE user_id = %(id)s
        ORDER BY log_date DESC LIMIT 10
    """, {'id': user_id}) or []
    return render_template('admin_dashboard.html', view='view_user',
                           user=user, goals=goals, logs=logs)


@app.route('/admin_create_user', methods=['GET', 'POST'])
def admin_create_user():
    if not _admin_required():
        return redirect(url_for('login'))
    if request.method == 'POST':
        username      = request.form.get('username', '').strip()
        email         = request.form.get('email', '').strip()
        first_name    = request.form.get('first_name', '').strip()
        last_name     = request.form.get('last_name', '').strip()
        password      = request.form.get('password', '').strip()
        dob           = request.form.get('date_of_birth') or None
        gender        = request.form.get('gender', 'Male')
        weight        = request.form.get('weight') or None
        height        = request.form.get('height') or None
        activity_level= request.form.get('activity_level', 'Moderate')
        if not username or not email or not password:
            flash('Username, email, and password are required.', 'danger')
            return render_template('admin_dashboard.html', view='create_user')
        existing = execute_query(
            "SELECT user_id FROM USERS WHERE username=%(u)s OR email=%(e)s",
            {'u': username, 'e': email})
        if existing:
            flash('Username or email already in use.', 'danger')
            return render_template('admin_dashboard.html', view='create_user')
        execute_query("""
            INSERT INTO USERS (username, email, password_hash, first_name, last_name,
                               date_of_birth, gender, weight, height, activity_level)
            VALUES (%(u)s,%(e)s,%(p)s,%(fn)s,%(ln)s,%(dob)s,%(g)s,%(w)s,%(h)s,%(al)s)
        """, {'u': username, 'e': email, 'p': password, 'fn': first_name,
              'ln': last_name, 'dob': dob, 'g': gender, 'w': weight,
              'h': height, 'al': activity_level}, fetch=False)
        flash(f'User {username} created successfully!', 'success')
        return redirect(url_for('admin_users'))
    return render_template('admin_dashboard.html', view='create_user')


@app.route('/admin_update_user/<int:user_id>', methods=['GET', 'POST'])
def admin_update_user(user_id):
    if not _admin_required():
        return redirect(url_for('login'))
    if request.method == 'POST':
        execute_query("""
            UPDATE USERS SET email=%(e)s, first_name=%(fn)s, last_name=%(ln)s,
                date_of_birth=%(dob)s, gender=%(g)s, weight=%(w)s,
                height=%(h)s, activity_level=%(al)s
            WHERE user_id=%(id)s
        """, {'e':  request.form.get('email','').strip(),
              'fn': request.form.get('first_name','').strip(),
              'ln': request.form.get('last_name','').strip(),
              'dob':request.form.get('date_of_birth') or None,
              'g':  request.form.get('gender','Male'),
              'w':  request.form.get('weight') or None,
              'h':  request.form.get('height') or None,
              'al': request.form.get('activity_level','Moderate'),
              'id': user_id}, fetch=False)
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    user = execute_query("""
        SELECT user_id, username, email, first_name, last_name,
               date_of_birth, gender, weight, height, activity_level,
               0, 'N/A'
        FROM USERS WHERE user_id = %(id)s
    """, {'id': user_id})
    user = user[0] if user else None
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_users'))
    return render_template('admin_dashboard.html', view='update_user', user=user)


@app.route('/admin_delete_user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM USERS WHERE user_id = %(id)s",
                  {'id': user_id}, fetch=False)
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin_delete_daily_log/<int:log_id>', methods=['POST'])
def admin_delete_daily_log(log_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM DAILY_LOG WHERE daily_log_id = %(id)s",
                  {'id': log_id}, fetch=False)
    flash('Daily log deleted.', 'success')
    return redirect(url_for('admin_daily_logs'))


@app.route('/admin_delete_meal_log/<int:log_id>', methods=['POST'])
def admin_delete_meal_log(log_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM MEAL_LOG WHERE meal_log_id = %(id)s",
                  {'id': log_id}, fetch=False)
    flash('Meal log deleted.', 'success')
    return redirect(url_for('admin_meal_logs'))


@app.route('/admin_delete_activity_log/<int:log_id>', methods=['POST'])
def admin_delete_activity_log(log_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM ACTIVITY_LOG WHERE activity_log_id = %(id)s",
                  {'id': log_id}, fetch=False)
    flash('Activity log deleted.', 'success')
    return redirect(url_for('admin_activity_logs'))


@app.route('/admin_delete_mood_log/<int:log_id>', methods=['POST'])
def admin_delete_mood_log(log_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM MOOD_LOG WHERE mood_log_id = %(id)s",
                  {'id': log_id}, fetch=False)
    flash('Mood log deleted.', 'success')
    return redirect(url_for('admin_mood_logs'))


@app.route('/admin_update_goal/<int:goal_id>', methods=['POST'])
def admin_update_goal(goal_id):
    if not _admin_required():
        return redirect(url_for('login'))
    status = request.form.get('status', 'Active')
    execute_query("UPDATE GOALS SET status=%(s)s WHERE goal_id=%(id)s",
                  {'s': status, 'id': goal_id}, fetch=False)
    flash('Goal status updated.', 'success')
    return redirect(url_for('admin_goals'))


@app.route('/admin_delete_goal/<int:goal_id>', methods=['POST'])
def admin_delete_goal(goal_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM GOALS WHERE goal_id = %(id)s",
                  {'id': goal_id}, fetch=False)
    flash('Goal deleted.', 'success')
    return redirect(url_for('admin_goals'))


@app.route('/admin_edit_meal/<int:meal_id>', methods=['GET', 'POST'])
def admin_edit_meal(meal_id):
    if not _admin_required():
        return redirect(url_for('login'))
    if request.method == 'POST':
        execute_query("""
            UPDATE MEALS SET meal_name=%(n)s, meal_category=%(c)s,
                calories=%(cal)s, protein=%(p)s, carbohydrates=%(cb)s,
                fats=%(f)s, fiber=%(fi)s
            WHERE meal_id=%(id)s
        """, {
            'n':   request.form.get('meal_name', '').strip(),
            'c':   request.form.get('meal_category', ''),
            'cal': request.form.get('calories', 0),
            'p':   request.form.get('protein', 0),
            'cb':  request.form.get('carbs', 0),
            'f':   request.form.get('fats', 0),
            'fi':  request.form.get('fiber', 0),
            'id':  meal_id
        }, fetch=False)
        flash('Meal updated successfully!', 'success')
        return redirect(url_for('admin_meals'))
    meal = execute_query(
        "SELECT meal_id, meal_name, meal_category, calories, protein, carbohydrates, fats, fiber FROM MEALS WHERE meal_id=%(id)s",
        {'id': meal_id}
    )
    meal = meal[0] if meal else None
    if not meal:
        flash('Meal not found.', 'danger')
        return redirect(url_for('admin_meals'))
    return render_template('admin_dashboard.html', view='edit_meal', meal=meal)


@app.route('/admin_delete_meal/<int:meal_id>', methods=['POST'])
def admin_delete_meal(meal_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM MEALS WHERE meal_id=%(id)s", {'id': meal_id}, fetch=False)
    flash('Meal deleted successfully.', 'success')
    return redirect(url_for('admin_meals'))


@app.route('/admin_edit_activity/<int:activity_id>', methods=['GET', 'POST'])
def admin_edit_activity(activity_id):
    if not _admin_required():
        return redirect(url_for('login'))
    if request.method == 'POST':
        execute_query("""
            UPDATE ACTIVITIES SET activity_name=%(n)s, activity_category=%(c)s,
                calories_per_minute=%(cpm)s, intensity_level=%(i)s,
                description=%(d)s
            WHERE activity_id=%(id)s
        """, {
            'n':   request.form.get('activity_name', '').strip(),
            'c':   request.form.get('activity_category', ''),
            'cpm': request.form.get('calories_per_minute', 0),
            'i':   request.form.get('intensity_level', 'Moderate'),
            'd':   request.form.get('description', ''),
            'id':  activity_id
        }, fetch=False)
        flash('Activity updated successfully!', 'success')
        return redirect(url_for('admin_activities'))
    activity = execute_query(
        "SELECT activity_id, activity_name, activity_category, calories_per_minute, intensity_level, COALESCE(description,'') FROM ACTIVITIES WHERE activity_id=%(id)s",
        {'id': activity_id}
    )
    activity = activity[0] if activity else None
    if not activity:
        flash('Activity not found.', 'danger')
        return redirect(url_for('admin_activities'))
    return render_template('admin_dashboard.html', view='edit_activity', activity=activity)


@app.route('/admin_delete_activity/<int:activity_id>', methods=['POST'])
def admin_delete_activity(activity_id):
    if not _admin_required():
        return redirect(url_for('login'))
    execute_query("DELETE FROM ACTIVITIES WHERE activity_id=%(id)s",
                  {'id': activity_id}, fetch=False)
    flash('Activity deleted successfully.', 'success')
    return redirect(url_for('admin_activities'))


@app.route('/admin_daily_logs')
def admin_daily_logs():
    if not _admin_required():
        return redirect(url_for('login'))
    daily_logs = execute_query("""
        SELECT dl.daily_log_id, u.username,
               TO_CHAR(dl.log_date,'YYYY-MM-DD'),
               dl.total_calories_consumed, dl.total_calories_burned,
               dl.water_intake, dl.sleep_hours, dl.weight
        FROM DAILY_LOG dl JOIN USERS u ON dl.user_id = u.user_id
        ORDER BY dl.log_date DESC LIMIT 200
    """) or []
    return render_template('admin_dashboard.html',
                           view='daily_logs', daily_logs=daily_logs)


@app.route('/admin_meal_logs')
def admin_meal_logs():
    if not _admin_required():
        return redirect(url_for('login'))
    meal_logs = execute_query("""
        SELECT ml.meal_log_id, u.username, m.meal_name,
               TO_CHAR(dl.log_date,'YYYY-MM-DD'),
               ml.quantity, ml.total_calories
        FROM MEAL_LOG ml
        JOIN DAILY_LOG dl ON ml.daily_log_id = dl.daily_log_id
        JOIN USERS u ON dl.user_id = u.user_id
        JOIN MEALS m ON ml.meal_id = m.meal_id
        ORDER BY ml.meal_log_id DESC LIMIT 200
    """) or []
    return render_template('admin_dashboard.html',
                           view='meal_logs', meal_logs=meal_logs)


@app.route('/admin_activity_logs')
def admin_activity_logs():
    if not _admin_required():
        return redirect(url_for('login'))
    activity_logs = execute_query("""
        SELECT al.activity_log_id, u.username, 'Exercise' AS activity_name,
               TO_CHAR(dl.log_date,'YYYY-MM-DD'),
               al.duration_minutes, al.calories_burned
        FROM ACTIVITY_LOG al
        JOIN DAILY_LOG dl ON al.daily_log_id = dl.daily_log_id
        JOIN USERS u ON dl.user_id = u.user_id
        ORDER BY al.activity_log_id DESC LIMIT 200
    """) or []
    return render_template('admin_dashboard.html',
                           view='activity_logs', activity_logs=activity_logs)


@app.route('/admin_mood_logs')
def admin_mood_logs():
    if not _admin_required():
        return redirect(url_for('login'))
    mood_logs = execute_query("""
        SELECT ml.mood_log_id, u.username, ml.mood_rating,
               ml.stress_level, ml.energy_level,
               '' AS notes, TO_CHAR(dl.log_date,'YYYY-MM-DD')
        FROM MOOD_LOG ml
        JOIN DAILY_LOG dl ON ml.daily_log_id = dl.daily_log_id
        JOIN USERS u ON dl.user_id = u.user_id
        ORDER BY ml.mood_log_id DESC LIMIT 200
    """) or []
    return render_template('admin_dashboard.html',
                           view='mood_logs', mood_logs=mood_logs)


@app.route('/admin_goals')
def admin_goals():
    if not _admin_required():
        return redirect(url_for('login'))
    goals = execute_query("""
        SELECT g.goal_id, u.username, g.goal_type,
               g.target_value, g.current_value, g.status,
               TO_CHAR(g.start_date,'YYYY-MM-DD'),
               TO_CHAR(g.target_date,'YYYY-MM-DD')
        FROM GOALS g JOIN USERS u ON g.user_id = u.user_id
        ORDER BY g.goal_id DESC LIMIT 200
    """) or []
    return render_template('admin_dashboard.html', view='goals', goals=goals)


@app.route('/admin_meals')
def admin_meals():
    if not _admin_required():
        return redirect(url_for('login'))
    meals = execute_query("""
        SELECT meal_id, meal_name, meal_category, calories,
               protein, carbohydrates, fats, fiber, NULL
        FROM MEALS ORDER BY meal_name LIMIT 500
    """) or []
    return render_template('admin_dashboard.html', view='meals', meals=meals)


@app.route('/admin_activities')
def admin_activities():
    if not _admin_required():
        return redirect(url_for('login'))
    activities = execute_query("""
        SELECT activity_id, activity_name, activity_category,
               calories_per_minute, intensity_level,
               COALESCE(description,'') AS description
        FROM ACTIVITIES ORDER BY activity_name LIMIT 500
    """) or []
    return render_template('admin_dashboard.html',
                           view='activities', activities=activities)


@app.route('/admin_add_meal', methods=['GET', 'POST'])
def admin_add_meal():
    if not _admin_required():
        return redirect(url_for('login'))
    if request.method == 'POST':
        meal_name = request.form.get('meal_name', '').strip()
        category  = request.form.get('meal_category', '')
        calories  = request.form.get('calories', 0)
        protein   = request.form.get('protein', 0)
        carbs     = request.form.get('carbs', 0)
        fats      = request.form.get('fats', 0)
        if not meal_name or not category:
            flash('Meal name and category are required.', 'danger')
        else:
            execute_query("""
                INSERT INTO MEALS
                    (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber)
                VALUES (%(n)s,%(c)s,%(cal)s,%(p)s,%(cb)s,%(f)s,0)
            """, {'n': meal_name, 'c': category, 'cal': calories,
                  'p': protein, 'cb': carbs, 'f': fats}, fetch=False)
            flash(f'Meal "{meal_name}" added successfully!', 'success')
    meals = execute_query("""
        SELECT meal_id, meal_name, meal_category, calories
        FROM MEALS ORDER BY meal_id DESC LIMIT 100
    """) or []
    return render_template('admin_dashboard.html', view='add_meal', meals=meals)


@app.route('/admin_add_activity', methods=['GET', 'POST'])
def admin_add_activity():
    if not _admin_required():
        return redirect(url_for('login'))
    if request.method == 'POST':
        activity_name = request.form.get('activity_name', '').strip()
        category      = request.form.get('activity_category', '')
        cpm           = request.form.get('calories_per_minute', 0)
        intensity     = request.form.get('intensity_level', 'Moderate')
        if not activity_name or not category:
            flash('Activity name and category are required.', 'danger')
        else:
            execute_query("""
                INSERT INTO ACTIVITIES
                    (activity_name, activity_category, calories_per_minute, intensity_level)
                VALUES (%(n)s,%(c)s,%(cpm)s,%(i)s)
            """, {'n': activity_name, 'c': category,
                  'cpm': cpm, 'i': intensity}, fetch=False)
            flash(f'Activity "{activity_name}" added successfully!', 'success')
    activities = execute_query("""
        SELECT activity_id, activity_name, activity_category, calories_per_minute
        FROM ACTIVITIES ORDER BY activity_id DESC LIMIT 100
    """) or []
    return render_template('admin_dashboard.html',
                           view='add_activity', activities=activities)


@app.route('/admin_suggestions')
def admin_suggestions():
    if not _admin_required():
        return redirect(url_for('login'))
    suggestions = execute_query("""
        SELECT s.suggestion_id, u.username, s.suggestion_type,
               s.suggestion_text, s.reasoning_type,
               'N/A', 'Active',
               TO_CHAR(s.created_date,'YYYY-MM-DD')
        FROM SUGGESTIONS s JOIN USERS u ON s.user_id = u.user_id
        ORDER BY s.suggestion_id DESC LIMIT 200
    """) or []
    return render_template('admin_dashboard.html',
                           view='suggestions', suggestions=suggestions)


@app.route('/admin_reports')
def admin_reports():
    if not _admin_required():
        return redirect(url_for('login'))
    reports = execute_query("""
        SELECT r.report_id, u.username, r.report_type,
               TO_CHAR(r.report_period_start,'YYYY-MM-DD'),
               TO_CHAR(r.report_period_end,'YYYY-MM-DD'),
               r.total_calories_consumed, r.total_calories_burned,
               r.average_weight, r.weight_change, r.goals_achieved,
               r.report_summary,
               TO_CHAR(r.generated_date,'YYYY-MM-DD')
        FROM REPORTS r JOIN USERS u ON r.user_id = u.user_id
        ORDER BY r.generated_date DESC LIMIT 200
    """) or []

    def safe_val(q, p=None):
        r = execute_query(q, p)
        return r[0][0] if r and r[0][0] is not None else 0

    ai_stats = {
        'total_reports':     safe_val("SELECT COUNT(*) FROM REPORTS"),
        'total_suggestions': safe_val("SELECT COUNT(*) FROM SUGGESTIONS"),
        'total_goals':       safe_val("SELECT COUNT(*) FROM GOALS"),
        'goals_completed':   safe_val("SELECT COUNT(*) FROM GOALS WHERE status='Completed'"),
        'goals_active':      safe_val("SELECT COUNT(*) FROM GOALS WHERE status='Active'"),
        'avg_mood':          safe_val("SELECT ROUND(AVG(mood_rating::numeric),1) FROM MOOD_LOG"),
        'total_users':       safe_val("SELECT COUNT(*) FROM USERS"),
        'users_with_goals':  safe_val("SELECT COUNT(DISTINCT user_id) FROM GOALS"),
    }
    top_goal = execute_query(
        "SELECT goal_type, COUNT(*) AS cnt FROM GOALS GROUP BY goal_type ORDER BY cnt DESC LIMIT 1"
    )
    ai_stats['top_goal_type'] = top_goal[0][0] if top_goal else 'N/A'

    return render_template('admin_dashboard.html',
                           view='reports', reports=reports, ai_stats=ai_stats)


# ── Non-admin password reset stubs (kept as redirects) ───────────────────────
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return redirect(url_for('login'))

@app.route('/verify_reset_code', methods=['GET', 'POST'])
def verify_reset_code():
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return redirect(url_for('login'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

