-- ============================================================================
-- Smart Diet & Lifestyle Planner - Stored Procedures
-- Database Layer: PL/SQL Procedures for Business Operations
-- ============================================================================

-- Author: [Your Name]
-- Date: [Current Date]
-- Description: Stored procedures for common database operations

-- ============================================================================
-- Procedure: sp_register_user
-- Description: Register a new user in the system
-- Parameters:
--   p_username: User's username
--   p_email: User's email
--   p_password_hash: Hashed password
--   p_first_name: First name
--   p_last_name: Last name
--   p_dob: Date of birth
--   p_gender: Gender
--   p_user_id: OUT parameter returning new user ID
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_register_user (
    p_username IN VARCHAR2,
    p_email IN VARCHAR2,
    p_password_hash IN VARCHAR2,
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_dob IN DATE,
    p_gender IN VARCHAR2,
    p_user_id OUT NUMBER
)
AS
BEGIN
    -- Insert new user
    -- Return user ID
    -- Handle exceptions
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_add_diet_log
-- Description: Add a complete diet log entry with food items
-- Parameters:
--   p_user_id: User ID
--   p_meal_type: Type of meal
--   p_log_date: Date of log
--   p_food_items: Array/table of food items
--   p_log_id: OUT parameter returning new log ID
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_add_diet_log (
    p_user_id IN NUMBER,
    p_meal_type IN VARCHAR2,
    p_log_date IN DATE,
    p_log_id OUT NUMBER
)
AS
BEGIN
    -- Insert diet log
    -- Calculate totals
    -- Return log ID
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_add_activity_log
-- Description: Log a physical activity
-- Parameters:
--   p_user_id: User ID
--   p_activity_type_id: Activity type
--   p_duration: Duration in minutes
--   p_intensity: Intensity level
--   p_activity_date: Date of activity
--   p_activity_log_id: OUT parameter returning new activity log ID
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_add_activity_log (
    p_user_id IN NUMBER,
    p_activity_type_id IN NUMBER,
    p_duration IN NUMBER,
    p_intensity IN VARCHAR2,
    p_activity_date IN DATE,
    p_activity_log_id OUT NUMBER
)
AS
    v_calories_burned NUMBER;
    v_user_weight NUMBER;
BEGIN
    -- Get user weight
    -- Calculate calories burned
    -- Insert activity log
    -- Return activity log ID
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_update_user_profile
-- Description: Update user health profile
-- Parameters:
--   p_user_id: User ID
--   p_weight: Current weight
--   p_height: Height
--   p_target_weight: Target weight
--   p_activity_level: Activity level
--   p_dietary_preferences: Dietary preferences
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_update_user_profile (
    p_user_id IN NUMBER,
    p_weight IN NUMBER,
    p_height IN NUMBER,
    p_target_weight IN NUMBER,
    p_activity_level IN VARCHAR2,
    p_dietary_preferences IN VARCHAR2
)
AS
    v_bmi NUMBER;
BEGIN
    -- Calculate BMI
    -- Update or insert profile
    -- Log weight change if different
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_generate_daily_summary
-- Description: Generate daily nutrition and activity summary
-- Parameters:
--   p_user_id: User ID
--   p_date: Date for summary
--   p_total_calories_in: OUT total calories consumed
--   p_total_calories_out: OUT total calories burned
--   p_net_calories: OUT net calorie balance
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_generate_daily_summary (
    p_user_id IN NUMBER,
    p_date IN DATE,
    p_total_calories_in OUT NUMBER,
    p_total_calories_out OUT NUMBER,
    p_net_calories OUT NUMBER
)
AS
BEGIN
    -- Sum calories from diet logs
    -- Sum calories from activity logs
    -- Calculate net calories
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_save_meal_plan
-- Description: Save an AI-generated meal plan
-- Parameters:
--   p_user_id: User ID
--   p_plan_name: Name of meal plan
--   p_start_date: Plan start date
--   p_end_date: Plan end date
--   p_daily_calories: Target daily calories
--   p_macros: Macro distribution
--   p_meal_plan_id: OUT parameter returning meal plan ID
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_save_meal_plan (
    p_user_id IN NUMBER,
    p_plan_name IN VARCHAR2,
    p_start_date IN DATE,
    p_end_date IN DATE,
    p_daily_calories IN NUMBER,
    p_protein_target IN NUMBER,
    p_carbs_target IN NUMBER,
    p_fats_target IN NUMBER,
    p_meal_plan_id OUT NUMBER
)
AS
BEGIN
    -- Deactivate old meal plans
    -- Insert new meal plan
    -- Return meal plan ID
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_track_weight
-- Description: Record weight measurement
-- Parameters:
--   p_user_id: User ID
--   p_weight: Weight measurement
--   p_measurement_date: Date of measurement
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_track_weight (
    p_user_id IN NUMBER,
    p_weight IN NUMBER,
    p_measurement_date IN DATE
)
AS
BEGIN
    -- Insert weight tracking record
    -- Update user profile
    -- Recalculate BMI
    NULL;
END;
/
*/

-- ============================================================================
-- Procedure: sp_delete_user
-- Description: Delete user and all related data
-- Parameters:
--   p_user_id: User ID to delete
-- ============================================================================
/*
CREATE OR REPLACE PROCEDURE sp_delete_user (
    p_user_id IN NUMBER
)
AS
BEGIN
    -- Delete from all related tables
    -- Delete user record
    -- Log deletion
    NULL;
END;
/
*/

-- ============================================================================
-- End of Stored Procedures Script
-- ============================================================================
