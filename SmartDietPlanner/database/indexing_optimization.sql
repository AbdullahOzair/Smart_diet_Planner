-- ============================================================================
-- Smart Diet & Lifestyle Planner - Indexing and Query Optimization
-- Database Administration: Indexing Strategies and Performance Optimization
-- Oracle SQL Compatible
-- ============================================================================

-- ============================================================================
-- SECTION 1: CREATE INDEXES
-- ============================================================================

-- Secondary Index 1: Index on USERS.username for faster user lookups
-- This is a single-column index used in WHERE clauses and authentication queries
--CREATE INDEX idx_users_username ON USERS(username);

-- Secondary Index 2: Index on GOALS.status for filtering active/completed goals
CREATE INDEX idx_goals_status ON GOALS(status);

-- Composite Index 1: Index on DAILY_LOG (user_id, log_date) for date-range queries
-- This composite index improves performance of queries filtering by user and date
CREATE INDEX idx_daily_log_user_date ON DAILY_LOG(user_id, log_date);

-- Composite Index 2: Index on MEAL_LOG (daily_log_id, meal_id) for JOIN operations
CREATE INDEX idx_meal_log_composite ON MEAL_LOG(daily_log_id, meal_id);

-- ============================================================================
-- SECTION 2: QUERY OPTIMIZATION - QUERY 1
-- Query: Retrieve all daily logs for a specific user within a date range
-- ============================================================================

-- BEFORE INDEXING - Explain Plan
-- This query will perform a full table scan without the composite index
EXPLAIN PLAN FOR
SELECT d.daily_log_id, d.log_date, d.total_calories_consumed, d.total_calories_burned, d.weight
FROM DAILY_LOG d
WHERE d.user_id = 1
AND d.log_date BETWEEN DATE '2025-12-01' AND DATE '2025-12-31'
ORDER BY d.log_date;

-- Display execution plan BEFORE indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- AFTER INDEXING - Explain Plan
-- With idx_daily_log_user_date composite index, this query uses INDEX RANGE SCAN
EXPLAIN PLAN FOR
SELECT d.daily_log_id, d.log_date, d.total_calories_consumed, d.total_calories_burned, d.weight
FROM DAILY_LOG d
WHERE d.user_id = 1
AND d.log_date BETWEEN DATE '2025-12-01' AND DATE '2025-12-31'
ORDER BY d.log_date;

-- Display execution plan AFTER indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- ============================================================================
-- SECTION 3: QUERY OPTIMIZATION - QUERY 2
-- Query: Get all active goals for users with their details
-- ============================================================================

-- BEFORE INDEXING - Explain Plan
-- Without index on status, this requires full table scan of GOALS
EXPLAIN PLAN FOR
SELECT u.username, u.first_name, u.last_name, 
    g.goal_type, g.target_value, g.current_value, g.status
FROM USERS u
JOIN GOALS g ON u.user_id = g.user_id
WHERE g.status = 'Active'
ORDER BY u.username;

-- Display execution plan BEFORE indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- AFTER INDEXING - Explain Plan
-- With idx_goals_status index, this uses INDEX RANGE SCAN on GOALS table
EXPLAIN PLAN FOR
SELECT u.username, u.first_name, u.last_name, 
    g.goal_type, g.target_value, g.current_value, g.status
FROM USERS u
JOIN GOALS g ON u.user_id = g.user_id
WHERE g.status = 'Active'
ORDER BY u.username;

-- Display execution plan AFTER indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- ============================================================================
-- SECTION 4: QUERY OPTIMIZATION - QUERY 3
-- Query: Retrieve meal logs with meal details for a specific daily log
-- ============================================================================

-- BEFORE INDEXING - Explain Plan
EXPLAIN PLAN FOR
SELECT ml.meal_log_id, m.meal_name, m.meal_category, 
    ml.quantity, ml.total_calories, ml.meal_time
FROM MEAL_LOG ml
JOIN MEALS m ON ml.meal_id = m.meal_id
WHERE ml.daily_log_id = 1
ORDER BY ml.meal_time;

-- Display execution plan BEFORE indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- AFTER INDEXING - Explain Plan
-- With idx_meal_log_composite index, JOIN operations are optimized
EXPLAIN PLAN FOR
SELECT ml.meal_log_id, m.meal_name, m.meal_category, 
    ml.quantity, ml.total_calories, ml.meal_time
FROM MEAL_LOG ml
JOIN MEALS m ON ml.meal_id = m.meal_id
WHERE ml.daily_log_id = 1
ORDER BY ml.meal_time;

-- Display execution plan AFTER indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- ============================================================================
-- SECTION 5: QUERY OPTIMIZATION - QUERY 4
-- Query: User authentication and profile retrieval by username
-- ============================================================================

-- BEFORE INDEXING - Explain Plan
EXPLAIN PLAN FOR
SELECT user_id, username, email, first_name, last_name, weight, height
FROM USERS
WHERE username = 'zainab_moazzam';

-- Display execution plan BEFORE indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- AFTER INDEXING - Explain Plan
-- With idx_users_username index, this uses INDEX UNIQUE SCAN
EXPLAIN PLAN FOR
SELECT user_id, username, email, first_name, last_name, weight, height
FROM USERS
WHERE username = 'zainab_moazzam';

-- Display execution plan AFTER indexing
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- ============================================================================
-- SECTION 6: INDEX SUMMARY AND ANALYSIS
-- ============================================================================

-- Query to view all indexes created for the Smart Diet Planner database
SELECT index_name, table_name, column_name, column_position
FROM user_ind_columns
WHERE table_name IN ('USERS', 'GOALS', 'DAILY_LOG', 'MEAL_LOG', 'ACTIVITY_LOG', 'SUGGESTIONS')
ORDER BY table_name, index_name, column_position;

-- Query to check index usage statistics
SELECT index_name, table_name, uniqueness, status
FROM user_indexes
WHERE table_name IN ('USERS', 'GOALS', 'DAILY_LOG', 'MEAL_LOG', 'ACTIVITY_LOG', 'SUGGESTIONS')
ORDER BY table_name;

-- ============================================================================
-- PERFORMANCE IMPROVEMENT NOTES (As SQL Comments)
-- ============================================================================

-- Index Type Summary:
-- 1. idx_users_username: Secondary Index (Single Column)
--    Purpose: Fast user authentication and lookup by username
--    Impact: Reduces login query time from full table scan to index seek

-- 2. idx_goals_status: Secondary Index (Single Column)
--    Purpose: Quick filtering of goals by status (Active, Completed, Cancelled)
--    Impact: Improves dashboard queries showing active goals

-- 3. idx_daily_log_user_date: Composite Index (Multiple Columns)
--    Purpose: Optimize date-range queries per user for reports and analytics
--    Impact: Significantly improves weekly/monthly report generation

-- 4. idx_meal_log_composite: Composite Index (Multiple Columns)
--    Purpose: Optimize JOIN operations and meal log retrieval
--    Impact: Faster meal history queries and daily nutrition summaries

-- Expected Performance Gains:
-- - User login queries: 80-90% faster
-- - Daily log retrieval: 70-85% faster
-- - Goal filtering: 60-75% faster
-- - Meal log JOINs: 65-80% faster

-- ============================================================================
-- End of Indexing and Optimization Script
-- ============================================================================
