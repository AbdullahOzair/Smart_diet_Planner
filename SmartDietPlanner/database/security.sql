-- ============================================================================
-- Smart Diet & Lifestyle Planner - PL/SQL Script
-- Phase 5: Security/ ROLES
-- Oracle PL/SQL Compatible
-- ============================================================================
-- Security
-- Create admin role
CREATE ROLE diet_admin;

-- Create user role
CREATE ROLE diet_user;
-- Admin privileges
GRANT SELECT, INSERT, UPDATE, DELETE ON USERS TO diet_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON GOALS TO diet_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON DAILY_LOG TO diet_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON MEAL_LOG TO diet_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ACTIVITY_LOG TO diet_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON SUGGESTIONS TO diet_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON REPORTS TO diet_admin;

-- User privileges (restricted)
GRANT SELECT, INSERT ON DAILY_LOG TO diet_user;
GRANT SELECT ON MEALS TO diet_user;
GRANT SELECT ON ACTIVITIES TO diet_user;
GRANT SELECT ON SUGGESTIONS TO diet_user;
GRANT SELECT ON REPORTS TO diet_user;

-- Create application admin user
CREATE USER zainab IDENTIFIED BY zainab123;
GRANT diet_admin TO zainab;

-- Create normal application user
CREATE USER ozair IDENTIFIED BY ozair123;
GRANT diet_user TO ozair;

-- Allow login
GRANT CREATE SESSION TO diet_admin_user;
GRANT CREATE SESSION TO diet_app_user;

-- Revoke delete access from normal user
REVOKE DELETE ON DAILY_LOG FROM diet_user;

