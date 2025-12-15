-- ============================================================================
-- Smart Diet & Lifestyle Planner - Database Triggers
-- Database Layer: PL/SQL Triggers for Automation and Data Integrity
-- ============================================================================

-- Author: [Your Name]
-- Date: [Current Date]
-- Description: Triggers for automating tasks and maintaining data integrity

-- ============================================================================
-- Trigger: trg_users_before_insert
-- Description: Auto-generate user ID and set default values before insert
-- Table: users
-- Timing: BEFORE INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_users_before_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    -- Generate user ID from sequence if not provided
    -- Set created_date to current timestamp
    -- Set is_active to 1 by default
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_user_profile_after_update
-- Description: Update BMI when weight or height changes
-- Table: user_profiles
-- Timing: BEFORE INSERT OR UPDATE
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_user_profile_after_update
BEFORE INSERT OR UPDATE ON user_profiles
FOR EACH ROW
BEGIN
    -- Recalculate BMI using weight and height
    -- Set updated_date to current timestamp
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_diet_log_before_insert
-- Description: Auto-generate log ID and calculate totals
-- Table: diet_logs
-- Timing: BEFORE INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_diet_log_before_insert
BEFORE INSERT ON diet_logs
FOR EACH ROW
BEGIN
    -- Generate log ID from sequence
    -- Set created_date to current timestamp
    -- Set log_time if not provided
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_diet_log_after_insert
-- Description: Update user statistics after diet log entry
-- Table: diet_logs
-- Timing: AFTER INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_diet_log_after_insert
AFTER INSERT ON diet_logs
FOR EACH ROW
BEGIN
    -- Update daily totals
    -- Check if calorie goal exceeded
    -- Generate suggestions if needed
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_activity_log_before_insert
-- Description: Calculate calories burned before inserting activity
-- Table: activity_logs
-- Timing: BEFORE INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_activity_log_before_insert
BEFORE INSERT ON activity_logs
FOR EACH ROW
DECLARE
    v_user_weight NUMBER;
    v_met_value NUMBER;
BEGIN
    -- Generate activity log ID
    -- Get user weight
    -- Get MET value for activity type
    -- Calculate calories burned if not provided
    -- Set created_date
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_weight_tracking_after_insert
-- Description: Update user profile with latest weight
-- Table: weight_tracking
-- Timing: AFTER INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_weight_tracking_after_insert
AFTER INSERT ON weight_tracking
FOR EACH ROW
BEGIN
    -- Update user profile with new weight
    -- Recalculate BMI
    -- Check if goal weight reached
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_meal_plan_before_insert
-- Description: Deactivate old meal plans before inserting new one
-- Table: meal_plans
-- Timing: BEFORE INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_meal_plan_before_insert
BEFORE INSERT ON meal_plans
FOR EACH ROW
BEGIN
    -- Generate meal plan ID
    -- Set created_date
    -- Set is_active to 1
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_meal_plan_after_insert
-- Description: Deactivate other meal plans after new plan inserted
-- Table: meal_plans
-- Timing: AFTER INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_meal_plan_after_insert
AFTER INSERT ON meal_plans
FOR EACH ROW
BEGIN
    -- Deactivate all other meal plans for this user
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_suggestion_before_insert
-- Description: Auto-generate suggestion ID and set defaults
-- Table: suggestions
-- Timing: BEFORE INSERT
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_suggestion_before_insert
BEFORE INSERT ON suggestions
FOR EACH ROW
BEGIN
    -- Generate suggestion ID
    -- Set created_date
    -- Set default status to 'Pending'
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_validate_diet_log_date
-- Description: Ensure diet log date is not in the future
-- Table: diet_logs
-- Timing: BEFORE INSERT OR UPDATE
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_validate_diet_log_date
BEFORE INSERT OR UPDATE ON diet_logs
FOR EACH ROW
BEGIN
    -- Check if log_date is not in future
    -- Raise error if invalid
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_validate_activity_date
-- Description: Ensure activity date is not in the future
-- Table: activity_logs
-- Timing: BEFORE INSERT OR UPDATE
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_validate_activity_date
BEFORE INSERT OR UPDATE ON activity_logs
FOR EACH ROW
BEGIN
    -- Check if activity_date is not in future
    -- Raise error if invalid
    NULL;
END;
/
*/

-- ============================================================================
-- Trigger: trg_audit_user_changes
-- Description: Log changes to user table for auditing
-- Table: users
-- Timing: AFTER UPDATE
-- ============================================================================
/*
CREATE OR REPLACE TRIGGER trg_audit_user_changes
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    -- Log old and new values to audit table
    -- Record timestamp and change type
    NULL;
END;
/
*/

-- ============================================================================
-- End of Triggers Script
-- ============================================================================
