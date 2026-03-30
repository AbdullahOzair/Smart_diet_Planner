"""
Migration script to add target_weight column to USERS table
and sync goal data from GOALS table
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from db import execute_query

try:
    print("🔄 Adding target_weight column to USERS table...")
    # Add the column (PostgreSQL syntax)
    execute_query("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS target_weight NUMERIC(5,2)
    """, fetch=False)
    print("✅ Column added successfully!")
except Exception as e:
    if "column already exists" in str(e).lower() or "duplicate column" in str(e).lower():
        print("✓ Column already exists - skipping")
    else:
        print(f"⚠️  Note: {e}")

try:
    print("\n🔄 Syncing target weights from GOALS to USERS...")
    # Sync target weights from GOALS table to USERS table (PostgreSQL)
    sync_query = """
        UPDATE users u SET 
            target_weight = g.target_value
        FROM goals g
        WHERE g.user_id = u.user_id 
        AND g.status = 'Active'
        AND g.goal_id = (
            SELECT goal_id FROM goals g2 
            WHERE g2.user_id = u.user_id 
            AND g2.status = 'Active'
            ORDER BY created_date DESC 
            LIMIT 1
        )
    """
    execute_query(sync_query, fetch=False)
    print("✅ Target weights synced successfully!")
    
    # Count how many users were updated
    result = execute_query("""
        SELECT COUNT(*) FROM users WHERE target_weight IS NOT NULL
    """)
    if result:
        count = result[0][0]
        print(f"   Updated {count} user(s) with target weight data")
        
except Exception as e:
    print(f"⚠️  Error during sync: {e}")

print("\n✅ Migration complete!")
