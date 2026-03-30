-- Add goal_speed column to GOALS table for intelligent goal speed tracking
ALTER TABLE GOALS ADD (
    goal_speed VARCHAR(20) DEFAULT 'Moderate' CHECK (goal_speed IN ('Slow & Healthy', 'Moderate', 'Aggressive'))
);

-- Command to run in SQL*Plus or SQL Developer:
-- @add_goal_speed_column.sql
