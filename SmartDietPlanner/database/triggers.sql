-- ============================================================================
-- Smart Diet & Lifestyle Planner - Database Triggers
-- Oracle PL/SQL Compatible
-- ============================================================================

-- Trigger 1: Automatically update total_calories_consumed in DAILY_LOG after MEAL_LOG insert
CREATE OR REPLACE TRIGGER update_daily_calories
AFTER INSERT ON MEAL_LOG
FOR EACH ROW
DECLARE
    v_total_calories NUMBER;
BEGIN
    -- Calculate total calories for the day
    SELECT NVL(SUM(total_calories), 0)
    INTO v_total_calories
    FROM MEAL_LOG
    WHERE daily_log_id = :NEW.daily_log_id;
    
    -- Update DAILY_LOG with new total
    UPDATE DAILY_LOG
    SET total_calories_consumed = v_total_calories
    WHERE daily_log_id = :NEW.daily_log_id;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20003, 'Error updating daily calories: ' || SQLERRM);
END update_daily_calories;
/

-- Trigger 2: Automatically change goal status to 'Completed' when target is reached
CREATE OR REPLACE TRIGGER check_goal_completion
BEFORE UPDATE ON GOALS
FOR EACH ROW
BEGIN
    -- Check if current_value has reached or exceeded target_value
    IF :NEW.current_value >= :NEW.target_value AND :OLD.status = 'Active' THEN
        :NEW.status := 'Completed';
        DBMS_OUTPUT.PUT_LINE('Goal completed for goal_id: ' || :NEW.goal_id);
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20004, 'Error checking goal completion: ' || SQLERRM);
END check_goal_completion;
/
---------------------------------------------------------------------------
-- END OF FILE
