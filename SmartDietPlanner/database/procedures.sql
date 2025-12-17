-- ============================================================================
-- Smart Diet & Lifestyle Planner - Stored Procedures
-- Oracle PL/SQL Compatible
-- ============================================================================

-- Procedure 1: Insert Daily Log with duplicate validation
CREATE OR REPLACE PROCEDURE insert_daily_log (
    p_user_id IN NUMBER,
    p_log_date IN DATE,
    p_calories_consumed IN NUMBER,
    p_calories_burned IN NUMBER,
    p_water_intake IN NUMBER,
    p_sleep_hours IN NUMBER,
    p_weight IN NUMBER,
    p_notes IN VARCHAR2
) AS
    v_count NUMBER;
BEGIN
    -- Check for duplicate entry
    SELECT COUNT(*)
    INTO v_count
    FROM DAILY_LOG
    WHERE user_id = p_user_id AND log_date = p_log_date;
    
    IF v_count > 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Daily log already exists for this user and date');
    END IF;
    
    -- Insert the daily log
    INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, 
                        water_intake, sleep_hours, weight, notes)
    VALUES (p_user_id, p_log_date, p_calories_consumed, p_calories_burned, 
            p_water_intake, p_sleep_hours, p_weight, p_notes);
    
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Daily log inserted successfully');
    
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('Error: Duplicate entry detected');
        ROLLBACK;
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        ROLLBACK;
END insert_daily_log;
/

-- Procedure 2: Insert AI Suggestion with validation
CREATE OR REPLACE PROCEDURE insert_suggestion (
    p_user_id IN NUMBER,
    p_suggestion_type IN VARCHAR2,
    p_suggestion_text IN VARCHAR2,
    p_reasoning IN VARCHAR2,
    p_priority IN VARCHAR2
) AS
    v_user_exists NUMBER;
BEGIN
    -- Validate user_id exists
    SELECT COUNT(*)
    INTO v_user_exists
    FROM USERS
    WHERE user_id = p_user_id;
    
    IF v_user_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Invalid user_id: User does not exist');
    END IF;
    
    -- Insert suggestion
    INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, reasoning, priority, status)
    VALUES (p_user_id, p_suggestion_type, p_suggestion_text, p_reasoning, p_priority, 'Pending');
    
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Suggestion inserted successfully');
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Error: User not found');
        ROLLBACK;
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        ROLLBACK;
END insert_suggestion;
/
---------------------------------------------------------------------------
-- END OF FILE
