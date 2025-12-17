-- ============================================================================
-- FILE: backup_recovery.sql
-- PURPOSE: Demonstrate logical backup and recovery in Oracle
-- PROJECT: Smart Diet & Lifestyle Planner
-- ============================================================================

-- ============================================================================
-- SECTION 1: LOGICAL BACKUP (EXPORT)
-- ============================================================================

-- Logical backup is performed using Oracle Data Pump Export (expdp)
-- This creates a backup of schema objects and data in a .dmp file

-- Example command to export the SmartDiet schema:

-- expdp system/password@ORCL schemas=SMARTDIET
-- directory=DATA_PUMP_DIR
-- dumpfile=smartdiet_backup.dmp
-- logfile=smartdiet_export.log

-- Explanation:
-- schemas=SMARTDIET     -> Exports all tables, views, procedures of schema
-- dumpfile              -> Backup file
-- logfile               -> Log file for export process
-- ============================================================================
-- SECTION 2: RECOVERY (IMPORT)
-- ============================================================================

-- Logical recovery is performed using Oracle Data Pump Import (impdp)
-- This restores the database objects from the backup file

-- Example command to restore the SmartDiet schema:

-- impdp system/password@ORCL schemas=SMARTDIET
-- directory=DATA_PUMP_DIR
-- dumpfile=smartdiet_backup.dmp
-- logfile=smartdiet_import.log

-- Explanation:
-- impdp restores tables, data, constraints, indexes, and PL/SQL objects
-- from the backup file into the database
-- ============================================================================
-- SECTION 3: DATA LOSS & RECOVERY SIMULATION
-- ============================================================================

-- Simulate accidental deletion
-- DELETE FROM USERS WHERE user_id = 1;

-- COMMIT;

-- After deletion, recovery would be done using the import command (impdp)
-- to restore the deleted data from backup
-- screenshot of terminal 
--exp system/password@SmartDiet file=smartdiet_backup.dmp full=y
--imp system/password@SmartDiet file=smartdiet_backup.dmp full=y