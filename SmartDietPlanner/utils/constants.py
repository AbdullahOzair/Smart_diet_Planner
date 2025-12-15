"""
Smart Diet & Lifestyle Planner - Constants
Utilities: Application-wide Constants and Configuration
"""

# ============================================================================
# Database Configuration
# ============================================================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service_name': 'ORCL',
    'username': 'diet_app_user',
    'password': 'your_password_here',  # Should be loaded from environment variable
}

# ============================================================================
# Application Settings
# ============================================================================
APP_NAME = "Smart Diet & Lifestyle Planner"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# ============================================================================
# User Settings
# ============================================================================
MIN_AGE = 13
MAX_AGE = 120
MIN_WEIGHT = 20.0  # kg
MAX_WEIGHT = 300.0  # kg
MIN_HEIGHT = 50.0  # cm
MAX_HEIGHT = 250.0  # cm

# ============================================================================
# Nutritional Constants
# ============================================================================
# Calories per gram
CALORIES_PER_GRAM_PROTEIN = 4
CALORIES_PER_GRAM_CARB = 4
CALORIES_PER_GRAM_FAT = 9

# Daily Recommended Intake (General Guidelines)
RECOMMENDED_PROTEIN_PERCENTAGE = 0.30  # 30% of total calories
RECOMMENDED_CARB_PERCENTAGE = 0.40     # 40% of total calories
RECOMMENDED_FAT_PERCENTAGE = 0.30      # 30% of total calories

# Calorie adjustment for goals
CALORIE_DEFICIT_WEIGHT_LOSS = 500    # Daily calorie deficit
CALORIE_SURPLUS_WEIGHT_GAIN = 500    # Daily calorie surplus

# ============================================================================
# BMI Categories
# ============================================================================
BMI_UNDERWEIGHT = 18.5
BMI_NORMAL_UPPER = 24.9
BMI_OVERWEIGHT_UPPER = 29.9
BMI_OBESE = 30.0

BMI_CATEGORIES = {
    'underweight': (0, 18.5),
    'normal': (18.5, 24.9),
    'overweight': (25.0, 29.9),
    'obese': (30.0, float('inf'))
}

# ============================================================================
# Activity Levels and Multipliers
# ============================================================================
ACTIVITY_LEVELS = {
    'sedentary': 1.2,      # Little or no exercise
    'light': 1.375,        # Light exercise 1-3 days/week
    'moderate': 1.55,      # Moderate exercise 3-5 days/week
    'very_active': 1.725,  # Heavy exercise 6-7 days/week
    'extra_active': 1.9    # Very heavy exercise, physical job
}

# ============================================================================
# Meal Types
# ============================================================================
MEAL_TYPES = [
    'breakfast',
    'lunch',
    'dinner',
    'snack'
]

# ============================================================================
# Goal Types
# ============================================================================
GOAL_TYPES = [
    'weight_loss',
    'weight_gain',
    'maintenance',
    'muscle_gain',
    'fat_loss'
]

# ============================================================================
# Activity Intensity Levels
# ============================================================================
INTENSITY_LEVELS = [
    'low',
    'medium',
    'high',
    'very_high'
]

# ============================================================================
# Gender Options
# ============================================================================
GENDER_OPTIONS = [
    'male',
    'female',
    'other'
]

# ============================================================================
# Dietary Preferences
# ============================================================================
DIETARY_PREFERENCES = [
    'none',
    'vegetarian',
    'vegan',
    'pescatarian',
    'keto',
    'paleo',
    'low_carb',
    'high_protein',
    'gluten_free',
    'dairy_free'
]

# ============================================================================
# Food Categories
# ============================================================================
FOOD_CATEGORIES = [
    'protein',
    'grain',
    'vegetable',
    'fruit',
    'dairy',
    'fat',
    'snack',
    'beverage'
]

# ============================================================================
# Report Types
# ============================================================================
REPORT_TYPES = [
    'daily',
    'weekly',
    'monthly',
    'custom'
]

# ============================================================================
# Date Formats
# ============================================================================
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DISPLAY_DATE_FORMAT = '%d/%m/%Y'
DISPLAY_DATETIME_FORMAT = '%d/%m/%Y %H:%M'

# ============================================================================
# File Paths
# ============================================================================
DATA_DIRECTORY = 'data/'
EXPORT_DIRECTORY = 'exports/'
LOG_DIRECTORY = 'logs/'

# ============================================================================
# UI Constants
# ============================================================================
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# ============================================================================
# Validation Regex Patterns
# ============================================================================
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$'
PHONE_REGEX = r'^\+?1?\d{9,15}$'

# ============================================================================
# AI Model Settings
# ============================================================================
AI_MODEL_NAME = 'gpt-3.5-turbo'  # or other model
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 500

# ============================================================================
# Fuzzy Logic Parameters
# ============================================================================
FUZZY_BMI_RANGES = {
    'underweight': (0, 18.5, 20),
    'normal': (18.5, 21.75, 24.9),
    'overweight': (23, 27, 29.9),
    'obese': (28, 35, 50)
}

# ============================================================================
# Logging Configuration
# ============================================================================
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'diet_planner.log'

# ============================================================================
# Session Settings
# ============================================================================
SESSION_TIMEOUT = 3600  # seconds (1 hour)
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # seconds (15 minutes)

# ============================================================================
# Export Formats
# ============================================================================
EXPORT_FORMATS = [
    'pdf',
    'excel',
    'csv',
    'json'
]

# ============================================================================
# Error Messages
# ============================================================================
ERROR_MESSAGES = {
    'invalid_credentials': 'Invalid username or password',
    'connection_error': 'Failed to connect to database',
    'invalid_input': 'Invalid input provided',
    'session_expired': 'Your session has expired. Please login again',
    'permission_denied': 'You do not have permission to perform this action',
}

# ============================================================================
# Success Messages
# ============================================================================
SUCCESS_MESSAGES = {
    'login_success': 'Login successful',
    'logout_success': 'Logged out successfully',
    'save_success': 'Data saved successfully',
    'update_success': 'Data updated successfully',
    'delete_success': 'Data deleted successfully',
}
