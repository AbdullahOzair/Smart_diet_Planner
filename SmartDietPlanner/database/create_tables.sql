-- ============================================================================
-- Smart Diet & Lifestyle Planner - Table Creation Script
-- Database Layer: Oracle SQL Schema Definition
-- ============================================================================

-- Author: [Your Name]
-- Date: [Current Date]
-- Description: Creates all tables for the Smart Diet Planner system

-- ============================================================================
-- Table: USERS
-- Description: Stores user account information
-- ============================================================================
/*
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(50) UNIQUE NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    date_of_birth DATE,
    gender VARCHAR2(10),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active NUMBER(1) DEFAULT 1
);
*/

-- ============================================================================
-- Table: USER_PROFILES
-- Description: Stores user health profile and physical attributes
-- ============================================================================
/*
CREATE TABLE user_profiles (
    profile_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    weight NUMBER(5,2),
    height NUMBER(5,2),
    target_weight NUMBER(5,2),
    bmi NUMBER(5,2),
    activity_level VARCHAR2(20),
    dietary_preferences VARCHAR2(100),
    allergies VARCHAR2(255),
    health_conditions VARCHAR2(255),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- ============================================================================
-- Table: USER_GOALS
-- Description: Stores user health and fitness goals
-- ============================================================================
/*
CREATE TABLE user_goals (
    goal_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    goal_type VARCHAR2(50),
    target_value NUMBER,
    current_value NUMBER,
    start_date DATE,
    target_date DATE,
    status VARCHAR2(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- ============================================================================
-- Table: FOOD_DATABASE
-- Description: Master food database with nutritional information
-- ============================================================================
/*
CREATE TABLE food_database (
    food_id NUMBER PRIMARY KEY,
    food_name VARCHAR2(100) NOT NULL,
    food_category VARCHAR2(50),
    serving_size VARCHAR2(50),
    calories NUMBER(6,2),
    protein NUMBER(6,2),
    carbohydrates NUMBER(6,2),
    fats NUMBER(6,2),
    fiber NUMBER(6,2),
    vitamins VARCHAR2(255),
    minerals VARCHAR2(255),
    is_verified NUMBER(1) DEFAULT 0
);
*/

-- ============================================================================
-- Table: DIET_LOGS
-- Description: Stores daily food intake logs
-- ============================================================================
/*
CREATE TABLE diet_logs (
    log_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    meal_type VARCHAR2(20),
    log_date DATE,
    log_time TIMESTAMP,
    total_calories NUMBER(6,2),
    total_protein NUMBER(6,2),
    total_carbs NUMBER(6,2),
    total_fats NUMBER(6,2),
    notes VARCHAR2(500),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- ============================================================================
-- Table: DIET_LOG_ITEMS
-- Description: Individual food items within a diet log entry
-- ============================================================================
/*
CREATE TABLE diet_log_items (
    log_item_id NUMBER PRIMARY KEY,
    log_id NUMBER REFERENCES diet_logs(log_id),
    food_id NUMBER REFERENCES food_database(food_id),
    quantity NUMBER(6,2),
    unit VARCHAR2(20),
    calories NUMBER(6,2),
    protein NUMBER(6,2),
    carbs NUMBER(6,2),
    fats NUMBER(6,2)
);
*/

-- ============================================================================
-- Table: ACTIVITY_TYPES
-- Description: Master table for activity types and calorie burn rates
-- ============================================================================
/*
CREATE TABLE activity_types (
    activity_type_id NUMBER PRIMARY KEY,
    activity_name VARCHAR2(100) NOT NULL,
    activity_category VARCHAR2(50),
    met_value NUMBER(4,2),
    description VARCHAR2(255)
);
*/

-- ============================================================================
-- Table: ACTIVITY_LOGS
-- Description: Stores physical activity logs
-- ============================================================================
/*
CREATE TABLE activity_logs (
    activity_log_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    activity_type_id NUMBER REFERENCES activity_types(activity_type_id),
    duration_minutes NUMBER(6,2),
    intensity VARCHAR2(20),
    calories_burned NUMBER(6,2),
    activity_date DATE,
    activity_time TIMESTAMP,
    notes VARCHAR2(500),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- ============================================================================
-- Table: MEAL_PLANS
-- Description: Stores AI-generated meal plans
-- ============================================================================
/*
CREATE TABLE meal_plans (
    meal_plan_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    plan_name VARCHAR2(100),
    start_date DATE,
    end_date DATE,
    daily_calories NUMBER(6,2),
    protein_target NUMBER(6,2),
    carbs_target NUMBER(6,2),
    fats_target NUMBER(6,2),
    is_active NUMBER(1) DEFAULT 1,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- ============================================================================
-- Table: SUGGESTIONS
-- Description: Stores AI-generated suggestions and recommendations
-- ============================================================================
/*
CREATE TABLE suggestions (
    suggestion_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    suggestion_type VARCHAR2(50),
    suggestion_text CLOB,
    reasoning CLOB,
    confidence_score NUMBER(3,2),
    status VARCHAR2(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_date TIMESTAMP,
    feedback VARCHAR2(500)
);
*/

-- ============================================================================
-- Table: WEIGHT_TRACKING
-- Description: Tracks user weight over time
-- ============================================================================
/*
CREATE TABLE weight_tracking (
    tracking_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    weight NUMBER(5,2),
    measurement_date DATE,
    notes VARCHAR2(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- ============================================================================
-- Sequences for auto-increment primary keys
-- ============================================================================
/*
CREATE SEQUENCE seq_user_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_profile_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_goal_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_food_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_log_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_log_item_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_activity_type_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_activity_log_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_meal_plan_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_suggestion_id START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_tracking_id START WITH 1 INCREMENT BY 1;
*/

-- ============================================================================
-- End of Table Creation Script
-- ============================================================================
