-- ============================================================================
-- Smart Diet & Lifestyle Planner - Sample Data Insertion Script
-- Database Layer: Populate tables with test data
-- ============================================================================

-- Author: [Your Name]
-- Date: [Current Date]
-- Description: Inserts sample data for testing and development

-- ============================================================================
-- Insert Sample Users
-- ============================================================================
/*
INSERT INTO users (user_id, username, email, password_hash, first_name, last_name, date_of_birth, gender)
VALUES (seq_user_id.NEXTVAL, 'john_doe', 'john@example.com', 'hashed_password_123', 'John', 'Doe', TO_DATE('1990-05-15', 'YYYY-MM-DD'), 'Male');

INSERT INTO users (user_id, username, email, password_hash, first_name, last_name, date_of_birth, gender)
VALUES (seq_user_id.NEXTVAL, 'jane_smith', 'jane@example.com', 'hashed_password_456', 'Jane', 'Smith', TO_DATE('1992-08-22', 'YYYY-MM-DD'), 'Female');

INSERT INTO users (user_id, username, email, password_hash, first_name, last_name, date_of_birth, gender)
VALUES (seq_user_id.NEXTVAL, 'mike_johnson', 'mike@example.com', 'hashed_password_789', 'Mike', 'Johnson', TO_DATE('1988-03-10', 'YYYY-MM-DD'), 'Male');
*/

-- ============================================================================
-- Insert Sample User Profiles
-- ============================================================================
/*
INSERT INTO user_profiles (profile_id, user_id, weight, height, target_weight, activity_level, dietary_preferences)
VALUES (seq_profile_id.NEXTVAL, 1, 75.5, 175.0, 70.0, 'Moderately Active', 'No restrictions');

INSERT INTO user_profiles (profile_id, user_id, weight, height, target_weight, activity_level, dietary_preferences)
VALUES (seq_profile_id.NEXTVAL, 2, 65.0, 165.0, 60.0, 'Lightly Active', 'Vegetarian');

INSERT INTO user_profiles (profile_id, user_id, weight, height, target_weight, activity_level, dietary_preferences)
VALUES (seq_profile_id.NEXTVAL, 3, 90.0, 180.0, 80.0, 'Very Active', 'High Protein');
*/

-- ============================================================================
-- Insert Sample Food Database Entries
-- ============================================================================
/*
INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Chicken Breast', 'Protein', '100g', 165, 31.0, 0, 3.6, 0);

INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Brown Rice', 'Grain', '100g', 112, 2.6, 24.0, 0.9, 1.8);

INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Broccoli', 'Vegetable', '100g', 34, 2.8, 7.0, 0.4, 2.6);

INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Salmon', 'Protein', '100g', 208, 20.0, 0, 13.0, 0);

INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Oatmeal', 'Grain', '100g', 389, 16.9, 66.0, 6.9, 10.6);

INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Apple', 'Fruit', '1 medium', 95, 0.5, 25.0, 0.3, 4.4);

INSERT INTO food_database (food_id, food_name, food_category, serving_size, calories, protein, carbohydrates, fats, fiber)
VALUES (seq_food_id.NEXTVAL, 'Greek Yogurt', 'Dairy', '100g', 59, 10.0, 3.6, 0.4, 0);
*/

-- ============================================================================
-- Insert Sample Activity Types
-- ============================================================================
/*
INSERT INTO activity_types (activity_type_id, activity_name, activity_category, met_value, description)
VALUES (seq_activity_type_id.NEXTVAL, 'Running', 'Cardio', 8.0, 'Running at moderate pace');

INSERT INTO activity_types (activity_type_id, activity_name, activity_category, met_value, description)
VALUES (seq_activity_type_id.NEXTVAL, 'Walking', 'Cardio', 3.5, 'Walking at normal pace');

INSERT INTO activity_types (activity_type_id, activity_name, activity_category, met_value, description)
VALUES (seq_activity_type_id.NEXTVAL, 'Weight Training', 'Strength', 6.0, 'General weight lifting');

INSERT INTO activity_types (activity_type_id, activity_name, activity_category, met_value, description)
VALUES (seq_activity_type_id.NEXTVAL, 'Cycling', 'Cardio', 7.5, 'Cycling at moderate pace');

INSERT INTO activity_types (activity_type_id, activity_name, activity_category, met_value, description)
VALUES (seq_activity_type_id.NEXTVAL, 'Swimming', 'Cardio', 8.0, 'Swimming laps');

INSERT INTO activity_types (activity_type_id, activity_name, activity_category, met_value, description)
VALUES (seq_activity_type_id.NEXTVAL, 'Yoga', 'Flexibility', 2.5, 'General yoga practice');
*/

-- ============================================================================
-- Insert Sample Diet Logs
-- ============================================================================
/*
INSERT INTO diet_logs (log_id, user_id, meal_type, log_date, total_calories, total_protein, total_carbs, total_fats)
VALUES (seq_log_id.NEXTVAL, 1, 'Breakfast', SYSDATE, 450, 25.0, 50.0, 15.0);

INSERT INTO diet_logs (log_id, user_id, meal_type, log_date, total_calories, total_protein, total_carbs, total_fats)
VALUES (seq_log_id.NEXTVAL, 1, 'Lunch', SYSDATE, 600, 40.0, 60.0, 20.0);

INSERT INTO diet_logs (log_id, user_id, meal_type, log_date, total_calories, total_protein, total_carbs, total_fats)
VALUES (seq_log_id.NEXTVAL, 2, 'Breakfast', SYSDATE, 350, 15.0, 45.0, 10.0);
*/

-- ============================================================================
-- Insert Sample Activity Logs
-- ============================================================================
/*
INSERT INTO activity_logs (activity_log_id, user_id, activity_type_id, duration_minutes, intensity, calories_burned, activity_date)
VALUES (seq_activity_log_id.NEXTVAL, 1, 1, 30, 'Medium', 350, SYSDATE);

INSERT INTO activity_logs (activity_log_id, user_id, activity_type_id, duration_minutes, intensity, calories_burned, activity_date)
VALUES (seq_activity_log_id.NEXTVAL, 2, 2, 45, 'Low', 180, SYSDATE);

INSERT INTO activity_logs (activity_log_id, user_id, activity_type_id, duration_minutes, intensity, calories_burned, activity_date)
VALUES (seq_activity_log_id.NEXTVAL, 3, 3, 60, 'High', 400, SYSDATE);
*/

-- ============================================================================
-- Insert Sample User Goals
-- ============================================================================
/*
INSERT INTO user_goals (goal_id, user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (seq_goal_id.NEXTVAL, 1, 'Weight Loss', 70.0, 75.5, SYSDATE, ADD_MONTHS(SYSDATE, 3), 'Active');

INSERT INTO user_goals (goal_id, user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (seq_goal_id.NEXTVAL, 2, 'Weight Loss', 60.0, 65.0, SYSDATE, ADD_MONTHS(SYSDATE, 2), 'Active');

INSERT INTO user_goals (goal_id, user_id, goal_type, target_value, current_value, start_date, target_date, status)
VALUES (seq_goal_id.NEXTVAL, 3, 'Muscle Gain', 85.0, 90.0, SYSDATE, ADD_MONTHS(SYSDATE, 6), 'Active');
*/

-- ============================================================================
-- Commit all changes
-- ============================================================================
/*
COMMIT;
*/

-- ============================================================================
-- End of Sample Data Insertion Script
-- ============================================================================
