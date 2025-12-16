-- ============================================================================
-- Smart Diet & Lifestyle Planner - Sample Data Insertion Script
-- Oracle SQL Compatible
-- ============================================================================

-- ============================================================================
-- Table: USERS
-- Insert sample users with complete profile information
-- ============================================================================
INSERT INTO USERS (username, email, password_hash, first_name, last_name, date_of_birth, gender, weight, height, activity_level, dietary_preference, health_condition)
VALUES ('zainab_moazzam', 'zainab.moazzam@email.com', 'hashed_password_123', 'Zainab', 'Moazzam', DATE '2004-08-26', 'Female', 52, 164.0, 'Moderate', 'Vegetarian', 'None');

INSERT INTO USERS (username, email, password_hash, first_name, last_name, date_of_birth, gender, weight, height, activity_level, dietary_preference, health_condition)
VALUES ('abdullah_ozair', 'abdullah.ozair@email.com', 'hashed_password_456', 'Abdullah', 'Ozair', DATE '2003-08-22', 'Male', 55.0, 175.0, 'Active', 'Non-Vegetarian', 'None');

INSERT INTO USERS (username, email, password_hash, first_name, last_name, date_of_birth, gender, weight, height, activity_level, dietary_preference, health_condition)
VALUES ('user3', 'user3@email.com', 'hashed_password_789', 'user', '3', DATE '2000-11-10', 'Male', 58.0, 160.0, 'Light', 'Vegan', 'Diabetes Type 2');

-- ============================================================================
-- Table: GOALS
-- Insert health and fitness goals for users
-- ============================================================================
INSERT INTO GOALS (user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (1, 'Maintain Weight', 52.0, 52.0, DATE '2025-12-01', DATE '2026-03-01', 'Active');

INSERT INTO GOALS (user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (1, 'Fitness', 10000.0, 6000.0, DATE '2025-12-01', DATE '2026-01-01', 'Active');

INSERT INTO GOALS (user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (2, 'Weight Gain', 60.0, 55.0, DATE '2025-11-15', DATE '2026-02-15', 'Active');

INSERT INTO GOALS (user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (3, 'Weight Loss', 55.0, 58.0, DATE '2025-12-10', DATE '2026-04-10', 'Active');

-- ============================================================================
-- Table: MEALS
-- Insert master meal data with nutritional information
-- ============================================================================
INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Oatmeal with Berries', 'Breakfast', 280.0, 8.0, 48.0, 6.0, 7.0, '1 bowl', 'Healthy breakfast option with fiber');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Scrambled Eggs', 'Breakfast', 220.0, 18.0, 3.0, 15.0, 0.0, '2 eggs', 'High protein breakfast');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Grilled Chicken Salad', 'Lunch', 350.0, 35.0, 15.0, 18.0, 5.0, '1 plate', 'Lean protein with vegetables');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Brown Rice with Lentils', 'Lunch', 320.0, 12.0, 58.0, 4.0, 8.0, '1 plate', 'Vegetarian protein source');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Grilled Fish with Vegetables', 'Dinner', 380.0, 40.0, 20.0, 15.0, 6.0, '1 plate', 'Omega-3 rich dinner');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Vegetable Stir Fry', 'Dinner', 290.0, 8.0, 42.0, 10.0, 7.0, '1 plate', 'Low calorie vegetarian dinner');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Apple with Peanut Butter', 'Snack', 180.0, 4.0, 20.0, 8.0, 4.0, '1 apple + 2 tbsp', 'Healthy snack option');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Greek Yogurt', 'Snack', 150.0, 15.0, 12.0, 4.0, 0.0, '1 cup', 'High protein snack');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Whole Wheat Sandwich', 'Lunch', 310.0, 14.0, 45.0, 8.0, 6.0, '1 sandwich', 'Balanced lunch option');

INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size, description)
VALUES ('Protein Smoothie', 'Breakfast', 250.0, 20.0, 30.0, 5.0, 3.0, '1 glass', 'Quick protein-rich breakfast');

-- ============================================================================
-- Table: ACTIVITIES
-- Insert master activity data with calorie burn rates
-- ============================================================================
INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Running', 'Cardio', 10.5, 'High', 'Outdoor or treadmill running');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Walking', 'Cardio', 4.0, 'Low', 'Brisk walking exercise');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Cycling', 'Cardio', 8.0, 'Moderate', 'Stationary or outdoor cycling');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Weight Training', 'Strength', 6.5, 'Moderate', 'Resistance training with weights');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Yoga', 'Flexibility', 3.5, 'Low', 'Stretching and flexibility exercise');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Swimming', 'Cardio', 9.0, 'High', 'Full body cardio workout');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Basketball', 'Sports', 7.5, 'High', 'Team sport activity');

INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level, description)
VALUES ('Jump Rope', 'Cardio', 11.0, 'Very High', 'High intensity cardio');

-- ============================================================================
-- Table: DAILY_LOG
-- Insert daily summary logs for users
-- ============================================================================
INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, water_intake, sleep_hours, weight, notes)
VALUES (1, DATE '2025-12-15', 1450.0, 320.0, 2.5, 7.5, 52.0, 'Good day with balanced vegetarian meals');

INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, water_intake, sleep_hours, weight, notes)
VALUES (1, DATE '2025-12-14', 1520.0, 280.0, 2.0, 7.0, 52.0, 'Felt energetic throughout the day');

INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, water_intake, sleep_hours, weight, notes)
VALUES (2, DATE '2025-12-15', 1900.0, 450.0, 3.0, 6.5, 55.2, 'Good workout session and protein intake');

INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, water_intake, sleep_hours, weight, notes)
VALUES (2, DATE '2025-12-14', 1850.0, 400.0, 2.8, 7.0, 55.0, 'Excellent training day');

INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, water_intake, sleep_hours, weight, notes)
VALUES (3, DATE '2025-12-15', 1600.0, 180.0, 2.2, 8.0, 57.8, 'Following vegan diet plan');

INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, water_intake, sleep_hours, weight, notes)
VALUES (3, DATE '2025-12-14', 1650.0, 140.0, 2.0, 7.5, 58.0, 'Managed blood sugar levels well');

-- ============================================================================
-- Table: MEAL_LOG
-- Insert individual meal entries linked to daily logs
-- ============================================================================
INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (1, 1, TIMESTAMP '2025-12-15 08:00:00', 1.0, 280.0, 'Breakfast at home');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (1, 3, TIMESTAMP '2025-12-15 13:00:00', 1.0, 350.0, 'Lunch at office');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (1, 6, TIMESTAMP '2025-12-15 19:30:00', 1.0, 290.0, 'Light dinner');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (1, 7, TIMESTAMP '2025-12-15 16:00:00', 1.0, 180.0, 'Evening snack');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (2, 10, TIMESTAMP '2025-12-14 08:30:00', 1.0, 250.0, 'Quick breakfast');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (2, 4, TIMESTAMP '2025-12-14 13:30:00', 1.0, 320.0, 'Vegetarian lunch');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (2, 6, TIMESTAMP '2025-12-14 20:00:00', 1.0, 290.0, 'Healthy dinner');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (3, 2, TIMESTAMP '2025-12-15 07:30:00', 1.0, 220.0, 'High protein breakfast');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (3, 5, TIMESTAMP '2025-12-15 13:00:00', 1.0, 380.0, 'Protein-rich lunch');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (3, 3, TIMESTAMP '2025-12-15 19:00:00', 1.0, 350.0, 'Balanced dinner');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (3, 8, TIMESTAMP '2025-12-15 11:00:00', 1.0, 150.0, 'Mid-morning snack');

INSERT INTO MEAL_LOG (daily_log_id, meal_id, meal_time, quantity, total_calories, notes)
VALUES (3, 8, TIMESTAMP '2025-12-15 16:00:00', 1.0, 150.0, 'Afternoon snack');

-- ============================================================================
-- Table: ACTIVITY_LOG
-- Insert individual activity entries linked to daily logs
-- ============================================================================
INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (1, 1, 30.0, 315.0, TIMESTAMP '2025-12-15 06:30:00', 'Morning run');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (2, 3, 35.0, 280.0, TIMESTAMP '2025-12-14 18:00:00', 'Evening cycling session');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (3, 1, 40.0, 420.0, TIMESTAMP '2025-12-15 06:00:00', 'Morning cardio');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (3, 4, 30.0, 195.0, TIMESTAMP '2025-12-15 17:00:00', 'Weight training session');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (4, 4, 45.0, 292.5, TIMESTAMP '2025-12-14 17:30:00', 'Strength training');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (4, 2, 25.0, 100.0, TIMESTAMP '2025-12-14 20:00:00', 'Post-dinner walk');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (5, 5, 45.0, 157.5, TIMESTAMP '2025-12-15 07:00:00', 'Morning yoga');

INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, activity_time, notes)
VALUES (6, 2, 40.0, 160.0, TIMESTAMP '2025-12-14 18:30:00', 'Evening walk');

-- ============================================================================
-- Table: MOOD_LOG
-- Insert mood and wellness tracking entries
-- ============================================================================
INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
VALUES (1, 4, 'Low', 'High', 'Felt great after morning run', TIMESTAMP '2025-12-15 21:00:00');

INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
VALUES (2, 4, 'Moderate', 'Moderate', 'Balanced day overall', TIMESTAMP '2025-12-14 21:30:00');

INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
VALUES (3, 5, 'Low', 'High', 'Excellent workout and energy', TIMESTAMP '2025-12-15 20:30:00');

INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
VALUES (4, 4, 'Moderate', 'High', 'Good progress with fitness', TIMESTAMP '2025-12-14 22:00:00');

INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
VALUES (5, 3, 'Moderate', 'Moderate', 'Feeling positive about weight gain goal', TIMESTAMP '2025-12-15 21:00:00');

INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes, log_time)
VALUES (6, 3, 'Low', 'Moderate', 'Steady progress with meal plan', TIMESTAMP '2025-12-14 20:30:00');

-- ============================================================================
-- Table: SUGGESTIONS
-- Insert AI-generated suggestions and recommendations
-- ============================================================================
INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (1, 'Diet', 'Include more plant-based protein sources like lentils and tofu', 'Vegetarian diet needs adequate protein for muscle maintenance', 'High', 'Pending');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (1, 'Exercise', 'Maintain current moderate activity level with regular cardio', 'Current weight is healthy, focus on fitness maintenance', 'Medium', 'Accepted');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (1, 'Lifestyle', 'Increase water intake to at least 3 liters daily', 'Adequate hydration supports metabolism and overall health', 'Medium', 'Pending');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (2, 'Diet', 'Increase protein and calorie intake to support healthy weight gain', 'Current weight is below ideal, need nutrient-dense meals', 'High', 'Accepted');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (2, 'Exercise', 'Continue strength training and add more resistance exercises', 'Building muscle mass supports healthy weight gain goals', 'High', 'Pending');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (2, 'Lifestyle', 'Ensure adequate rest and recovery between workouts', 'Recovery is crucial for muscle growth and weight gain', 'Medium', 'Completed');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (3, 'Diet', 'Focus on low glycemic vegan foods to manage blood sugar', 'Important for diabetes management with vegan diet', 'High', 'Accepted');

INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
VALUES (3, 'Health', 'Monitor blood sugar levels regularly and maintain light activity', 'Consistent monitoring helps optimize vegan diet for diabetes control', 'High', 'Pending');

-- ============================================================================
-- Table: REPORTS
-- Insert generated health and progress reports
-- ============================================================================
INSERT INTO REPORTS (user_id, report_type, report_period_start, report_period_end, total_calories_consumed, total_calories_burned, average_weight, weight_change, goals_achieved, report_summary)
VALUES (1, 'Weekly', DATE '2025-12-08', DATE '2025-12-14', 10360.0, 2100.0, 52.0, 0.0, 1, 'Excellent weight maintenance. Vegetarian diet well balanced. Continue current approach.');

INSERT INTO REPORTS (user_id, report_type, report_period_start, report_period_end, total_calories_consumed, total_calories_burned, average_weight, weight_change, goals_achieved, report_summary)
VALUES (2, 'Weekly', DATE '2025-12-08', DATE '2025-12-14', 13150.0, 3150.0, 55.1, 0.2, 1, 'Positive weight gain progress. High activity level maintained. Increase protein intake.');

INSERT INTO REPORTS (user_id, report_type, report_period_start, report_period_end, total_calories_consumed, total_calories_burned, average_weight, weight_change, goals_achieved, report_summary)
VALUES (3, 'Weekly', DATE '2025-12-08', DATE '2025-12-14', 11450.0, 1260.0, 57.9, -0.2, 1, 'Good progress on weight loss. Blood sugar levels stable. Vegan diet working well.');

INSERT INTO REPORTS (user_id, report_type, report_period_start, report_period_end, total_calories_consumed, total_calories_burned, average_weight, weight_change, goals_achieved, report_summary)
VALUES (1, 'Monthly', DATE '2025-11-15', DATE '2025-12-14', 44800.0, 8800.0, 52.0, 0.0, 2, 'Monthly goals achieved. Weight stable and healthy. Fitness levels excellent.');

COMMIT;
