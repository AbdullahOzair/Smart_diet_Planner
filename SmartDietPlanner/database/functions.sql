-- ============================================================================
-- Smart Diet & Lifestyle Planner - Stored Functions
-- Oracle PL/SQL Compatible
-- ============================================================================

-- Function 1: Calculate BMI for a user
CREATE OR REPLACE FUNCTION calculate_bmi (
    p_user_id IN NUMBER
) RETURN NUMBER AS
    v_weight NUMBER;
    v_height NUMBER;
    v_bmi NUMBER;
BEGIN
    -- Get weight and height from USERS table
    SELECT weight, height
    INTO v_weight, v_height
    FROM USERS
    WHERE user_id = p_user_id;
    
    -- Calculate BMI: weight(kg) / (height(m) * height(m))
    -- Height is stored in cm, so convert to meters
    v_bmi := v_weight / POWER((v_height / 100), 2);
    
    RETURN ROUND(v_bmi, 2);
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN ZERO_DIVIDE THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RETURN NULL;
END calculate_bmi;
/

-- Function 2: Calculate calorie balance for a daily log
CREATE OR REPLACE FUNCTION calculate_calorie_balance (
    p_daily_log_id IN NUMBER
) RETURN NUMBER AS
    v_consumed NUMBER;
    v_burned NUMBER;
    v_balance NUMBER;
BEGIN
    -- Get calories consumed and burned from DAILY_LOG
    SELECT total_calories_consumed, total_calories_burned
    INTO v_consumed, v_burned
    FROM DAILY_LOG
    WHERE daily_log_id = p_daily_log_id;
    
    -- Calculate balance
    v_balance := v_consumed - v_burned;
    
    RETURN v_balance;
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RETURN NULL;
END calculate_calorie_balance;
/
---------------------------------------------------------------------------
-- END OF FILE