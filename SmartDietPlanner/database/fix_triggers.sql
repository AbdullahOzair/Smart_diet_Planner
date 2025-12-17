-- ============================================================================
-- Fix Mutating Table Error in Triggers
-- ============================================================================

-- Drop the old trigger
DROP TRIGGER update_daily_calories;
/

-- Create a new trigger that avoids mutating table error
-- This trigger updates the daily calories by adding the new meal's calories
CREATE OR REPLACE TRIGGER update_daily_calories
AFTER INSERT ON MEAL_LOG
FOR EACH ROW
BEGIN
    -- Update DAILY_LOG by adding the new meal's calories to existing total
    UPDATE DAILY_LOG
    SET total_calories_consumed = NVL(total_calories_consumed, 0) + :NEW.total_calories
    WHERE daily_log_id = :NEW.daily_log_id;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20003, 'Error updating daily calories: ' || SQLERRM);
END update_daily_calories;
/

-- Similarly, create trigger for activity log calories
CREATE OR REPLACE TRIGGER update_daily_activity_calories
AFTER INSERT ON ACTIVITY_LOG
FOR EACH ROW
BEGIN
    -- Update DAILY_LOG by adding the new activity's burned calories to existing total
    UPDATE DAILY_LOG
    SET total_calories_burned = NVL(total_calories_burned, 0) + :NEW.calories_burned
    WHERE daily_log_id = :NEW.daily_log_id;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20005, 'Error updating activity calories: ' || SQLERRM);
END update_daily_activity_calories;
/

COMMIT;
