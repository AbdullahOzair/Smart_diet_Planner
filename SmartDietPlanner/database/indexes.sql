-- ============================================================================
-- Smart Diet & Lifestyle Planner - Database Indexes
-- Database Layer: Index Creation for Performance Optimization
-- ============================================================================

-- Author: [Your Name]
-- Date: [Current Date]
-- Description: Creates indexes to improve query performance

-- ============================================================================
-- Indexes on USERS table
-- ============================================================================
/*
-- Index on username for fast user lookup during login
CREATE INDEX idx_users_username ON users(username);

-- Index on email for email-based queries
CREATE INDEX idx_users_email ON users(email);

-- Index on is_active for filtering active users
CREATE INDEX idx_users_active ON users(is_active);
*/

-- ============================================================================
-- Indexes on USER_PROFILES table
-- ============================================================================
/*
-- Index on user_id for joining with users table
CREATE INDEX idx_profiles_user_id ON user_profiles(user_id);

-- Index on activity_level for filtering and grouping
CREATE INDEX idx_profiles_activity_level ON user_profiles(activity_level);
*/

-- ============================================================================
-- Indexes on DIET_LOGS table
-- ============================================================================
/*
-- Composite index on user_id and log_date for daily queries
CREATE INDEX idx_diet_logs_user_date ON diet_logs(user_id, log_date);

-- Index on meal_type for meal-specific queries
CREATE INDEX idx_diet_logs_meal_type ON diet_logs(meal_type);

-- Index on log_date for date range queries
CREATE INDEX idx_diet_logs_date ON diet_logs(log_date);
*/

-- ============================================================================
-- Indexes on DIET_LOG_ITEMS table
-- ============================================================================
/*
-- Index on log_id for joining with diet_logs
CREATE INDEX idx_log_items_log_id ON diet_log_items(log_id);

-- Index on food_id for food-based analysis
CREATE INDEX idx_log_items_food_id ON diet_log_items(food_id);
*/

-- ============================================================================
-- Indexes on ACTIVITY_LOGS table
-- ============================================================================
/*
-- Composite index on user_id and activity_date for user activity queries
CREATE INDEX idx_activity_logs_user_date ON activity_logs(user_id, activity_date);

-- Index on activity_type_id for activity type analysis
CREATE INDEX idx_activity_logs_type ON activity_logs(activity_type_id);

-- Index on activity_date for date range queries
CREATE INDEX idx_activity_logs_date ON activity_logs(activity_date);
*/

-- ============================================================================
-- Indexes on FOOD_DATABASE table
-- ============================================================================
/*
-- Index on food_name for text search
CREATE INDEX idx_food_name ON food_database(food_name);

-- Index on food_category for category-based filtering
CREATE INDEX idx_food_category ON food_database(food_category);

-- Full-text index on food_name for better search performance (if supported)
-- CREATE INDEX idx_food_name_text ON food_database(food_name) INDEXTYPE IS CTXSYS.CONTEXT;
*/

-- ============================================================================
-- Indexes on MEAL_PLANS table
-- ============================================================================
/*
-- Composite index on user_id and is_active for active meal plan queries
CREATE INDEX idx_meal_plans_user_active ON meal_plans(user_id, is_active);

-- Index on start_date and end_date for date range queries
CREATE INDEX idx_meal_plans_dates ON meal_plans(start_date, end_date);
*/

-- ============================================================================
-- Indexes on SUGGESTIONS table
-- ============================================================================
/*
-- Composite index on user_id and status for pending suggestions
CREATE INDEX idx_suggestions_user_status ON suggestions(user_id, status);

-- Index on suggestion_type for type-based filtering
CREATE INDEX idx_suggestions_type ON suggestions(suggestion_type);

-- Index on created_date for chronological queries
CREATE INDEX idx_suggestions_date ON suggestions(created_date);
*/

-- ============================================================================
-- Indexes on WEIGHT_TRACKING table
-- ============================================================================
/*
-- Composite index on user_id and measurement_date for trend analysis
CREATE INDEX idx_weight_tracking_user_date ON weight_tracking(user_id, measurement_date);

-- Index on measurement_date for date-based queries
CREATE INDEX idx_weight_tracking_date ON weight_tracking(measurement_date);
*/

-- ============================================================================
-- Indexes on USER_GOALS table
-- ============================================================================
/*
-- Composite index on user_id and status for active goals
CREATE INDEX idx_user_goals_user_status ON user_goals(user_id, status);

-- Index on goal_type for goal type analysis
CREATE INDEX idx_user_goals_type ON user_goals(goal_type);

-- Index on target_date for deadline tracking
CREATE INDEX idx_user_goals_target_date ON user_goals(target_date);
*/

-- ============================================================================
-- Indexes on ACTIVITY_TYPES table
-- ============================================================================
/*
-- Index on activity_name for lookup
CREATE INDEX idx_activity_types_name ON activity_types(activity_name);

-- Index on activity_category for category filtering
CREATE INDEX idx_activity_types_category ON activity_types(activity_category);
*/

-- ============================================================================
-- Performance Analysis Comments
-- ============================================================================
/*
Performance Considerations:
1. Composite indexes are created for commonly used query patterns
2. Date-based indexes support reporting and analytics queries
3. Foreign key columns are indexed for join performance
4. Text search indexes improve food search functionality
5. Status-based indexes optimize filtering active records

Maintenance Notes:
- Monitor index usage with Oracle's index monitoring features
- Rebuild fragmented indexes periodically
- Consider partitioning for large tables (diet_logs, activity_logs)
- Use EXPLAIN PLAN to verify index usage in queries
*/

-- ============================================================================
-- End of Indexes Script
-- ============================================================================
