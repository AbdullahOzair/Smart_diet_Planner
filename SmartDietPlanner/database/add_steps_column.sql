-- Add steps column to ACTIVITY_LOG table
-- This script adds step tracking capability to activities

ALTER TABLE ACTIVITY_LOG 
ADD COLUMN steps NUMERIC(8,0) DEFAULT 0 CHECK (steps >= 0);

-- Update existing records to calculate steps from duration if walking/running
-- Assume average: 100 steps/min for walking, 160 steps/min for running
UPDATE ACTIVITY_LOG al
SET steps = CASE 
    WHEN a.activity_name ILIKE '%walk%' THEN ROUND(al.duration_minutes * 100)
    WHEN a.activity_name ILIKE '%run%' THEN ROUND(al.duration_minutes * 160)
    ELSE 0
END
FROM ACTIVITIES a
WHERE al.activity_id = a.activity_id;

-- Verification query - check the update
SELECT al.activity_log_id, a.activity_name, al.duration_minutes, al.steps
FROM ACTIVITY_LOG al
JOIN ACTIVITIES a ON al.activity_id = a.activity_id
WHERE al.steps > 0
LIMIT 10;
