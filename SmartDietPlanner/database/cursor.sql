-- ============================================================================
-- Smart Diet & Lifestyle Planner - PL/SQL Script
-- Phase 3: Cursor with Exception Handling
-- Oracle PL/SQL Compatible
-- ============================================================================

-- ============================================================================
-- CURSOR EXAMPLE WITH EXCEPTION HANDLING
-- ============================================================================

-- Cursor: Display all users with their latest weight from DAILY_LOG
DECLARE
    CURSOR user_weight_cursor IS
        SELECT u.user_id, u.username, d.weight, d.log_date
        FROM USERS u
        LEFT JOIN (
            SELECT user_id, weight, log_date,
                ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY log_date DESC) as rn
            FROM DAILY_LOG
        ) d ON u.user_id = d.user_id AND d.rn = 1
        ORDER BY u.username;
    
    v_user_id USERS.user_id%TYPE;
    v_username USERS.username%TYPE;
    v_weight DAILY_LOG.weight%TYPE;
    v_log_date DAILY_LOG.log_date%TYPE;
    
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== User Weight Report ===');
    DBMS_OUTPUT.PUT_LINE('');
    
    -- Open and loop through cursor
    OPEN user_weight_cursor;
    
    LOOP
        FETCH user_weight_cursor INTO v_user_id, v_username, v_weight, v_log_date;
        EXIT WHEN user_weight_cursor%NOTFOUND;
        
        IF v_weight IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('User: ' || v_username || 
                        ' | Latest Weight: ' || v_weight || ' kg' ||
                        ' | Date: ' || TO_CHAR(v_log_date, 'DD-MON-YYYY'));
        ELSE
            DBMS_OUTPUT.PUT_LINE('User: ' || v_username || ' | No weight data available');
        END IF;
    END LOOP;
    
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Total users processed: ' || user_weight_cursor%ROWCOUNT);
    
    -- Close cursor
    CLOSE user_weight_cursor;
    
EXCEPTION
    WHEN OTHERS THEN
        IF user_weight_cursor%ISOPEN THEN
            CLOSE user_weight_cursor;
        END IF;
        DBMS_OUTPUT.PUT_LINE('Error in cursor processing: ' || SQLERRM);
END;
/

-- ============================================================================
-- End of PL/SQL Script
-- ============================================================================
