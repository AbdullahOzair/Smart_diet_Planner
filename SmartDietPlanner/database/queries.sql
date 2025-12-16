-- ============================================================================
-- Smart Diet & Lifestyle Planner - SQL Queries
-- Phase 2: Query Collection for SmartDiet Planner
-- Oracle SQL Compatible
-- ============================================================================

-- ============================================================================
-- SECTION 1: BASIC SELECT QUERIES
-- ============================================================================
-- USERS table
SELECT * FROM users;

-- GOALS table
SELECT * FROM goals;

-- MEALS table
SELECT * FROM meals;

-- ACTIVITIES table
SELECT * FROM activities;

-- DAILY_LOG table
SELECT * FROM daily_log;

-- MEAL_LOG table
SELECT * FROM meal_log;

-- ACTIVITY_LOG table
SELECT * FROM activity_log;

-- MOOD_LOG table
SELECT * FROM mood_log;

-- SUGGESTIONS table
SELECT * FROM suggestions;

-- REPORTS table
SELECT * FROM reports;

-- Q1: Get all active goals
SELECT goal_id, user_id, goal_type, target_value, current_value, status
FROM GOALS
WHERE status = 'Active';

-- Q2: List all meals with calories greater than 300
SELECT meal_name, meal_category, calories, protein, carbohydrates
FROM MEALS
WHERE calories > 300
ORDER BY calories DESC;

-- Q3: Find all high-intensity activities
SELECT activity_name, activity_category, calories_per_minute, intensity_level
FROM ACTIVITIES
WHERE intensity_level IN ('High', 'Very High')
ORDER BY calories_per_minute DESC;


-- Q4: Retrieve all pending suggestions
SELECT suggestion_id, user_id, suggestion_type, suggestion_text, priority
FROM SUGGESTIONS
WHERE status = 'Pending'
ORDER BY priority DESC;

-- ============================================================================
-- SECTION 2: JOIN QUERIES
-- ============================================================================

-- Q1: Get user details with their goals
SELECT u.username, u.first_name, u.last_name, g.goal_type, g.target_value, g.status
FROM USERS u
JOIN GOALS g ON u.user_id = g.user_id
ORDER BY u.username, g.goal_type;

-- Q2: Show meal logs with meal details
SELECT d.log_date, m.meal_name, m.meal_category, ml.quantity, ml.total_calories
FROM MEAL_LOG ml
JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
JOIN MEALS m ON ml.meal_id = m.meal_id
ORDER BY d.log_date DESC, ml.meal_time;

-- Q3: Get mood logs with user and daily log information
SELECT u.username, d.log_date, ml.mood_rating, ml.stress_level, ml.energy_level, ml.notes
FROM MOOD_LOG ml
JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
JOIN USERS u ON d.user_id = u.user_id
ORDER BY d.log_date DESC;

-- Q4: List users with their suggestions
SELECT u.username, s.suggestion_type, s.suggestion_text, s.priority, s.status
FROM USERS u
JOIN SUGGESTIONS s ON u.user_id = s.user_id
WHERE s.status != 'Rejected'
ORDER BY u.username, s.priority DESC;

-- ============================================================================
-- SECTION 3: GROUP BY & HAVING QUERIES
-- ============================================================================

-- Q1: Count goals by goal type
SELECT goal_type, COUNT(*) as total_goals, AVG(target_value) as avg_target
FROM GOALS
GROUP BY goal_type
ORDER BY total_goals DESC;

-- Q2: Calculate average calories by meal category abd rounding the value to 2 decimal places
SELECT meal_category, 
    COUNT(*) AS meal_count,
    ROUND(AVG(calories), 2) AS avg_calories,
    ROUND(AVG(protein), 2) AS avg_protein
FROM MEALS
GROUP BY meal_category
ORDER BY avg_calories DESC;


-- Q3: Count suggestions by type and status
SELECT suggestion_type, status, COUNT(*) as suggestion_count
FROM SUGGESTIONS
GROUP BY suggestion_type, status
ORDER BY suggestion_type, status;

-- Q4: Find users with more than 1 active goal
SELECT u.username, COUNT(g.goal_id) as active_goals
FROM USERS u
JOIN GOALS g ON u.user_id = g.user_id
WHERE g.status = 'Active'
GROUP BY u.username
HAVING COUNT(g.goal_id) > 1;

-- Q5: Activity categories with average calorie burn rate greater than 7
SELECT activity_category, 
    COUNT(*) as activity_count,
    AVG(calories_per_minute) as avg_cal_per_min
FROM ACTIVITIES
GROUP BY activity_category
HAVING AVG(calories_per_minute) > 7
ORDER BY avg_cal_per_min DESC;

-- ============================================================================
-- SECTION 4: VIEWS
-- ============================================================================

-- Q1: Create view for user health overview
CREATE OR REPLACE VIEW user_health_overview AS
SELECT u.user_id, 
    u.username, 
    u.weight, 
    u.height,
    u.activity_level,
    u.dietary_preference,
    COUNT(DISTINCT g.goal_id) as total_goals
FROM USERS u
LEFT JOIN GOALS g ON u.user_id = g.user_id
GROUP BY u.user_id, u.username, u.weight, u.height, u.activity_level, u.dietary_preference;

-- Q2: Create view for daily nutrition summary
CREATE OR REPLACE VIEW daily_nutrition_summary AS
SELECT d.daily_log_id,
    d.user_id,
    d.log_date,
    d.total_calories_consumed,
    d.total_calories_burned,
    d.water_intake,
    d.sleep_hours,
    (d.total_calories_consumed - d.total_calories_burned) as calorie_balance
FROM DAILY_LOG d;

-- Q3: Create view for meal statistics
CREATE OR REPLACE VIEW meal_statistics AS
SELECT m.meal_category,
    COUNT(*) as total_meals,
    AVG(m.calories) as avg_calories,
    MIN(m.calories) as min_calories,
    MAX(m.calories) as max_calories,
    AVG(m.protein) as avg_protein
FROM MEALS m
GROUP BY m.meal_category;

-- ============================================================================
-- SECTION 5: ANALYTICAL FUNCTIONS (Window/Partition Functions)
-- ============================================================================

-- Q1: Rank users by weight within each gender
SELECT username, gender, weight,
    RANK() OVER (PARTITION BY gender ORDER BY weight DESC) as weight_rank
FROM USERS;

-- Q2: Calculate running total of calories consumed per user
SELECT u.username, 
    d.log_date, 
    d.total_calories_consumed,
    SUM(d.total_calories_consumed) OVER (PARTITION BY u.user_id ORDER BY d.log_date) as running_total
FROM USERS u
JOIN DAILY_LOG d ON u.user_id = d.user_id
ORDER BY u.username, d.log_date;


-- Q3: Rank meals by calories within each category
SELECT meal_name, 
    meal_category, 
    calories,
    DENSE_RANK() OVER (PARTITION BY meal_category ORDER BY calories DESC) as calorie_rank
FROM MEALS;

-- Q4: Calculate average mood rating with moving average
SELECT u.username,
    d.log_date,
    ml.mood_rating,
    AVG(ml.mood_rating) OVER (PARTITION BY u.user_id ORDER BY d.log_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_mood
FROM MOOD_LOG ml
JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
JOIN USERS u ON d.user_id = u.user_id
ORDER BY u.username, d.log_date;

-- ============================================================================
-- End of Queries
-- ============================================================================
