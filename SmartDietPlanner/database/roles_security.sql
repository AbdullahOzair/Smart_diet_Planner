-- ============================================================================
-- Smart Diet & Lifestyle Planner - Roles and Security
-- Database Layer: User Roles, Privileges, and Security Configuration
-- ============================================================================

-- Author: [Your Name]
-- Date: [Current Date]
-- Description: Sets up database security with roles and privileges

-- ============================================================================
-- Create Database Roles
-- ============================================================================

-- ============================================================================
-- Role: DIET_ADMIN
-- Description: Full administrative access to all database objects
-- ============================================================================
/*
CREATE ROLE diet_admin;
*/

-- ============================================================================
-- Role: DIET_USER
-- Description: Standard user access for application users
-- ============================================================================
/*
CREATE ROLE diet_user;
*/

-- ============================================================================
-- Role: DIET_ANALYST
-- Description: Read-only access for data analysis and reporting
-- ============================================================================
/*
CREATE ROLE diet_analyst;
*/

-- ============================================================================
-- Role: DIET_API
-- Description: Application API access with limited privileges
-- ============================================================================
/*
CREATE ROLE diet_api;
*/

-- ============================================================================
-- Grant Privileges to DIET_ADMIN Role
-- ============================================================================
/*
-- Full control over all tables
GRANT ALL PRIVILEGES ON users TO diet_admin;
GRANT ALL PRIVILEGES ON user_profiles TO diet_admin;
GRANT ALL PRIVILEGES ON user_goals TO diet_admin;
GRANT ALL PRIVILEGES ON food_database TO diet_admin;
GRANT ALL PRIVILEGES ON diet_logs TO diet_admin;
GRANT ALL PRIVILEGES ON diet_log_items TO diet_admin;
GRANT ALL PRIVILEGES ON activity_types TO diet_admin;
GRANT ALL PRIVILEGES ON activity_logs TO diet_admin;
GRANT ALL PRIVILEGES ON meal_plans TO diet_admin;
GRANT ALL PRIVILEGES ON suggestions TO diet_admin;
GRANT ALL PRIVILEGES ON weight_tracking TO diet_admin;

-- Grant access to sequences
GRANT SELECT, ALTER ON seq_user_id TO diet_admin;
GRANT SELECT, ALTER ON seq_profile_id TO diet_admin;
GRANT SELECT, ALTER ON seq_goal_id TO diet_admin;
GRANT SELECT, ALTER ON seq_food_id TO diet_admin;
GRANT SELECT, ALTER ON seq_log_id TO diet_admin;
GRANT SELECT, ALTER ON seq_log_item_id TO diet_admin;
GRANT SELECT, ALTER ON seq_activity_type_id TO diet_admin;
GRANT SELECT, ALTER ON seq_activity_log_id TO diet_admin;
GRANT SELECT, ALTER ON seq_meal_plan_id TO diet_admin;
GRANT SELECT, ALTER ON seq_suggestion_id TO diet_admin;
GRANT SELECT, ALTER ON seq_tracking_id TO diet_admin;

-- Grant execution on procedures and functions
GRANT EXECUTE ON sp_register_user TO diet_admin;
GRANT EXECUTE ON sp_add_diet_log TO diet_admin;
GRANT EXECUTE ON sp_add_activity_log TO diet_admin;
GRANT EXECUTE ON sp_update_user_profile TO diet_admin;
GRANT EXECUTE ON sp_generate_daily_summary TO diet_admin;
GRANT EXECUTE ON sp_save_meal_plan TO diet_admin;
GRANT EXECUTE ON sp_track_weight TO diet_admin;
GRANT EXECUTE ON sp_delete_user TO diet_admin;
*/

-- ============================================================================
-- Grant Privileges to DIET_USER Role
-- ============================================================================
/*
-- Read and write access to user-specific data
GRANT SELECT, INSERT, UPDATE ON users TO diet_user;
GRANT SELECT, INSERT, UPDATE ON user_profiles TO diet_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_goals TO diet_user;
GRANT SELECT ON food_database TO diet_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON diet_logs TO diet_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON diet_log_items TO diet_user;
GRANT SELECT ON activity_types TO diet_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON activity_logs TO diet_user;
GRANT SELECT, INSERT, UPDATE ON meal_plans TO diet_user;
GRANT SELECT, INSERT, UPDATE ON suggestions TO diet_user;
GRANT SELECT, INSERT ON weight_tracking TO diet_user;

-- Grant access to sequences (SELECT only for regular users)
GRANT SELECT ON seq_log_id TO diet_user;
GRANT SELECT ON seq_log_item_id TO diet_user;
GRANT SELECT ON seq_activity_log_id TO diet_user;
GRANT SELECT ON seq_meal_plan_id TO diet_user;
GRANT SELECT ON seq_suggestion_id TO diet_user;
GRANT SELECT ON seq_tracking_id TO diet_user;

-- Grant execution on user-facing procedures
GRANT EXECUTE ON sp_add_diet_log TO diet_user;
GRANT EXECUTE ON sp_add_activity_log TO diet_user;
GRANT EXECUTE ON sp_update_user_profile TO diet_user;
GRANT EXECUTE ON sp_generate_daily_summary TO diet_user;
GRANT EXECUTE ON sp_track_weight TO diet_user;
GRANT EXECUTE ON fn_calculate_bmi TO diet_user;
GRANT EXECUTE ON fn_calculate_bmr TO diet_user;
GRANT EXECUTE ON fn_calculate_tdee TO diet_user;
*/

-- ============================================================================
-- Grant Privileges to DIET_ANALYST Role
-- ============================================================================
/*
-- Read-only access to all tables for analysis
GRANT SELECT ON users TO diet_analyst;
GRANT SELECT ON user_profiles TO diet_analyst;
GRANT SELECT ON user_goals TO diet_analyst;
GRANT SELECT ON food_database TO diet_analyst;
GRANT SELECT ON diet_logs TO diet_analyst;
GRANT SELECT ON diet_log_items TO diet_analyst;
GRANT SELECT ON activity_types TO diet_analyst;
GRANT SELECT ON activity_logs TO diet_analyst;
GRANT SELECT ON meal_plans TO diet_analyst;
GRANT SELECT ON suggestions TO diet_analyst;
GRANT SELECT ON weight_tracking TO diet_analyst;

-- Grant execution on query functions
GRANT EXECUTE ON fn_get_daily_calorie_intake TO diet_analyst;
GRANT EXECUTE ON fn_get_daily_calories_burned TO diet_analyst;
GRANT EXECUTE ON fn_get_average_weight TO diet_analyst;
GRANT EXECUTE ON fn_check_nutritional_balance TO diet_analyst;
*/

-- ============================================================================
-- Grant Privileges to DIET_API Role
-- ============================================================================
/*
-- API-specific access for application layer
GRANT SELECT, INSERT, UPDATE ON users TO diet_api;
GRANT SELECT, INSERT, UPDATE ON user_profiles TO diet_api;
GRANT SELECT, INSERT, UPDATE, DELETE ON diet_logs TO diet_api;
GRANT SELECT, INSERT, UPDATE, DELETE ON diet_log_items TO diet_api;
GRANT SELECT, INSERT, UPDATE, DELETE ON activity_logs TO diet_api;
GRANT SELECT ON food_database TO diet_api;
GRANT SELECT ON activity_types TO diet_api;
GRANT SELECT, INSERT, UPDATE ON meal_plans TO diet_api;
GRANT SELECT, INSERT, UPDATE ON suggestions TO diet_api;
GRANT SELECT, INSERT ON weight_tracking TO diet_api;

-- Grant execution on API procedures
GRANT EXECUTE ON sp_register_user TO diet_api;
GRANT EXECUTE ON sp_add_diet_log TO diet_api;
GRANT EXECUTE ON sp_add_activity_log TO diet_api;
GRANT EXECUTE ON sp_update_user_profile TO diet_api;
GRANT EXECUTE ON sp_save_meal_plan TO diet_api;
GRANT EXECUTE ON sp_track_weight TO diet_api;
*/

-- ============================================================================
-- Create Application Users and Assign Roles
-- ============================================================================

-- ============================================================================
-- Admin User
-- ============================================================================
/*
CREATE USER diet_db_admin IDENTIFIED BY "SecureAdminPass123!";
GRANT diet_admin TO diet_db_admin;
GRANT CONNECT, RESOURCE TO diet_db_admin;
*/

-- ============================================================================
-- Application User (for the Python application)
-- ============================================================================
/*
CREATE USER diet_app_user IDENTIFIED BY "SecureAppPass123!";
GRANT diet_api TO diet_app_user;
GRANT CONNECT TO diet_app_user;
*/

-- ============================================================================
-- Analyst User
-- ============================================================================
/*
CREATE USER diet_analyst_user IDENTIFIED BY "SecureAnalystPass123!";
GRANT diet_analyst TO diet_analyst_user;
GRANT CONNECT TO diet_analyst_user;
*/

-- ============================================================================
-- Security Policies
-- ============================================================================

-- ============================================================================
-- Enable Row-Level Security (Virtual Private Database)
-- Description: Ensure users can only access their own data
-- ============================================================================
/*
-- Create security policy function
CREATE OR REPLACE FUNCTION fn_user_security_policy (
    schema_var IN VARCHAR2,
    table_var IN VARCHAR2
)
RETURN VARCHAR2
IS
    v_predicate VARCHAR2(400);
BEGIN
    -- Return predicate to filter by current user
    v_predicate := 'user_id = SYS_CONTEXT(''USERENV'', ''SESSION_USER'')';
    RETURN v_predicate;
END;
/

-- Apply security policy to sensitive tables
BEGIN
    DBMS_RLS.ADD_POLICY (
        object_schema   => 'YOUR_SCHEMA',
        object_name     => 'DIET_LOGS',
        policy_name     => 'diet_logs_security_policy',
        function_schema => 'YOUR_SCHEMA',
        policy_function => 'fn_user_security_policy',
        statement_types => 'SELECT, INSERT, UPDATE, DELETE'
    );
END;
/
*/

-- ============================================================================
-- Password Policy
-- ============================================================================
/*
-- Set password complexity requirements
ALTER PROFILE DEFAULT LIMIT
    PASSWORD_LIFE_TIME 90
    PASSWORD_GRACE_TIME 7
    PASSWORD_REUSE_TIME 365
    PASSWORD_REUSE_MAX 5
    FAILED_LOGIN_ATTEMPTS 5
    PASSWORD_LOCK_TIME 1;
*/

-- ============================================================================
-- Audit Configuration
-- ============================================================================
/*
-- Enable auditing for sensitive operations
AUDIT INSERT, UPDATE, DELETE ON users BY ACCESS;
AUDIT INSERT, UPDATE, DELETE ON user_profiles BY ACCESS;
AUDIT SELECT ON diet_logs BY ACCESS;
AUDIT SELECT ON activity_logs BY ACCESS;
*/

-- ============================================================================
-- Encryption (if using Oracle Advanced Security)
-- ============================================================================
/*
-- Enable Transparent Data Encryption for sensitive columns
-- ALTER TABLE users MODIFY (password_hash ENCRYPT);
-- ALTER TABLE users MODIFY (email ENCRYPT);
*/

-- ============================================================================
-- Security Best Practices Comments
-- ============================================================================
/*
Security Guidelines:
1. Change default passwords immediately after setup
2. Use strong passwords with complexity requirements
3. Implement SSL/TLS for database connections
4. Regularly audit user access and privileges
5. Enable database activity monitoring
6. Implement backup and recovery procedures
7. Keep Oracle database patched and updated
8. Use separate accounts for different application tiers
9. Limit direct database access to necessary personnel
10. Implement data masking for non-production environments

Additional Recommendations:
- Use Oracle Wallet for credential management
- Enable Oracle Database Vault for advanced security
- Implement Oracle Data Redaction for sensitive data
- Set up Oracle Audit Vault for comprehensive auditing
- Use VPN for remote database access
*/

-- ============================================================================
-- End of Roles and Security Script
-- ============================================================================
