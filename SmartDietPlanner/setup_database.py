"""
Smart Diet Planner - Database Setup Script
Creates a clean, professional dataset with unique entries
"""
import psycopg2
import os
from datetime import datetime, timedelta
import random

try:
    conn = psycopg2.connect(
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432'),
        database=os.getenv('PG_DATABASE', 'smart_diet_planner'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASSWORD', 'postgres')
    )
    cursor = conn.cursor()
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

print("=" * 50)
print("SMART DIET PLANNER - DATABASE SETUP")
print("=" * 50)

# Step 1: Clean ALL existing data
print("\n[1/4] Cleaning existing data...")
tables_to_clean = ['MOOD_LOG', 'ACTIVITY_LOG', 'MEAL_LOG', 'DAILY_LOG', 'GOALS', 'SUGGESTIONS', 'REPORTS', 'ACTIVITIES', 'MEALS', 'USERS']
for table in tables_to_clean:
    try:
        # Keep admin user (user_id = 1) if exists
        if table == 'USERS':
            cursor.execute(f"DELETE FROM {table} WHERE user_id > 1")
        else:
            cursor.execute(f"DELETE FROM {table}")
        conn.commit()
        print(f"   ✓ Cleaned {table}")
    except Exception as e:
        conn.rollback()
        print(f"   ! {table}: {e}")

# Step 2: Insert UNIQUE MEALS (100+ unique food items)
print("\n[2/4] Inserting meals...")
meals = [
    # Breakfast Items (20)
    ('Scrambled Eggs', 'Breakfast', 147, 10, 11, 1, 0, '2 eggs'),
    ('Oatmeal with Honey', 'Breakfast', 180, 6, 32, 3, 4, '1 bowl'),
    ('Greek Yogurt Parfait', 'Breakfast', 200, 15, 28, 5, 2, '1 cup'),
    ('Avocado Toast', 'Breakfast', 240, 8, 22, 15, 6, '2 slices'),
    ('Pancakes with Maple Syrup', 'Breakfast', 350, 8, 60, 10, 2, '3 pancakes'),
    ('French Toast', 'Breakfast', 280, 9, 35, 12, 1, '2 slices'),
    ('Breakfast Burrito', 'Breakfast', 420, 18, 45, 20, 4, '1 burrito'),
    ('Smoothie Bowl', 'Breakfast', 250, 8, 45, 5, 6, '1 bowl'),
    ('Egg Benedict', 'Breakfast', 380, 18, 25, 24, 1, '1 serving'),
    ('Bagel with Cream Cheese', 'Breakfast', 300, 10, 45, 10, 2, '1 bagel'),
    ('Waffles with Berries', 'Breakfast', 320, 8, 50, 10, 3, '2 waffles'),
    ('Chia Pudding', 'Breakfast', 180, 6, 25, 8, 10, '1 cup'),
    ('Muesli with Milk', 'Breakfast', 220, 8, 40, 5, 5, '1 bowl'),
    ('Poached Eggs on Toast', 'Breakfast', 250, 14, 20, 12, 2, '2 eggs'),
    ('Banana Nut Oatmeal', 'Breakfast', 280, 8, 48, 8, 5, '1 bowl'),
    ('Vegetable Omelette', 'Breakfast', 200, 16, 8, 12, 2, '3 eggs'),
    ('Granola with Yogurt', 'Breakfast', 280, 10, 42, 10, 4, '1 bowl'),
    ('Breakfast Quesadilla', 'Breakfast', 380, 20, 32, 18, 3, '1 quesadilla'),
    ('Cottage Cheese with Fruit', 'Breakfast', 180, 14, 20, 5, 2, '1 cup'),
    ('Croissant with Jam', 'Breakfast', 280, 5, 35, 14, 1, '1 croissant'),
    
    # Lunch Items (25)
    ('Grilled Chicken Salad', 'Lunch', 350, 35, 15, 18, 5, '1 plate'),
    ('Turkey Club Sandwich', 'Lunch', 450, 28, 40, 22, 4, '1 sandwich'),
    ('Caesar Salad with Shrimp', 'Lunch', 380, 30, 18, 22, 4, '1 plate'),
    ('Vegetable Stir Fry', 'Lunch', 280, 12, 35, 12, 6, '1 plate'),
    ('Tuna Wrap', 'Lunch', 380, 28, 32, 16, 4, '1 wrap'),
    ('Minestrone Soup', 'Lunch', 180, 8, 28, 4, 6, '1 bowl'),
    ('Chicken Noodle Soup', 'Lunch', 200, 15, 22, 6, 2, '1 bowl'),
    ('Falafel Pita', 'Lunch', 420, 15, 50, 18, 8, '1 pita'),
    ('Caprese Salad', 'Lunch', 280, 14, 12, 22, 2, '1 plate'),
    ('Mushroom Risotto', 'Lunch', 380, 10, 55, 14, 3, '1 plate'),
    ('Grilled Cheese Sandwich', 'Lunch', 350, 15, 32, 20, 2, '1 sandwich'),
    ('Lentil Soup', 'Lunch', 220, 12, 35, 4, 10, '1 bowl'),
    ('Quinoa Buddha Bowl', 'Lunch', 420, 18, 52, 18, 10, '1 bowl'),
    ('BLT Sandwich', 'Lunch', 380, 18, 32, 22, 3, '1 sandwich'),
    ('Greek Salad', 'Lunch', 280, 10, 18, 20, 5, '1 plate'),
    ('Chicken Quesadilla', 'Lunch', 450, 28, 38, 24, 3, '1 quesadilla'),
    ('Tomato Basil Soup', 'Lunch', 180, 4, 28, 6, 4, '1 bowl'),
    ('Hummus with Pita', 'Lunch', 320, 12, 42, 14, 8, '1 serving'),
    ('Cobb Salad', 'Lunch', 420, 32, 15, 28, 5, '1 plate'),
    ('Veggie Burger', 'Lunch', 380, 18, 42, 16, 6, '1 burger'),
    ('Fish Tacos', 'Lunch', 420, 24, 38, 20, 4, '3 tacos'),
    ('Pasta Primavera', 'Lunch', 400, 14, 58, 14, 6, '1 plate'),
    ('Spinach Artichoke Wrap', 'Lunch', 380, 15, 40, 18, 5, '1 wrap'),
    ('Black Bean Soup', 'Lunch', 240, 14, 38, 4, 12, '1 bowl'),
    ('Mediterranean Wrap', 'Lunch', 400, 18, 42, 18, 6, '1 wrap'),
    
    # Dinner Items (25)
    ('Grilled Salmon', 'Dinner', 380, 40, 0, 22, 0, '200g'),
    ('Beef Steak with Vegetables', 'Dinner', 480, 45, 15, 28, 4, '250g'),
    ('Chicken Parmesan', 'Dinner', 520, 42, 30, 28, 3, '1 serving'),
    ('Shrimp Scampi', 'Dinner', 420, 32, 35, 18, 2, '1 plate'),
    ('Lamb Chops', 'Dinner', 450, 38, 0, 32, 0, '200g'),
    ('Roasted Turkey Breast', 'Dinner', 350, 48, 0, 16, 0, '200g'),
    ('Baked Cod with Herbs', 'Dinner', 280, 35, 8, 12, 2, '200g'),
    ('Pork Tenderloin', 'Dinner', 380, 40, 5, 22, 1, '200g'),
    ('Vegetable Lasagna', 'Dinner', 420, 18, 48, 18, 6, '1 serving'),
    ('Chicken Tikka Masala', 'Dinner', 450, 35, 28, 24, 4, '1 plate'),
    ('Beef Tacos', 'Dinner', 480, 28, 42, 26, 5, '3 tacos'),
    ('Spaghetti Bolognese', 'Dinner', 520, 28, 62, 20, 5, '1 plate'),
    ('Grilled Tuna Steak', 'Dinner', 320, 42, 0, 16, 0, '200g'),
    ('Stuffed Bell Peppers', 'Dinner', 350, 22, 32, 16, 6, '2 peppers'),
    ('Duck Breast', 'Dinner', 420, 32, 0, 32, 0, '180g'),
    ('Eggplant Parmesan', 'Dinner', 380, 15, 35, 22, 8, '1 serving'),
    ('Seafood Paella', 'Dinner', 480, 35, 52, 18, 4, '1 plate'),
    ('Chicken Marsala', 'Dinner', 420, 38, 18, 22, 2, '1 serving'),
    ('Beef Stroganoff', 'Dinner', 480, 32, 35, 28, 3, '1 plate'),
    ('Teriyaki Salmon', 'Dinner', 400, 38, 18, 20, 1, '200g'),
    ('Moroccan Chicken', 'Dinner', 420, 35, 28, 22, 5, '1 serving'),
    ('Thai Green Curry', 'Dinner', 450, 28, 32, 28, 4, '1 plate'),
    ('Herb Roasted Chicken', 'Dinner', 380, 42, 5, 22, 1, '1 quarter'),
    ('Meatloaf with Gravy', 'Dinner', 450, 32, 25, 28, 2, '1 slice'),
    ('Baked Ziti', 'Dinner', 480, 24, 52, 24, 4, '1 plate'),
    
    # Snacks (20)
    ('Apple Slices with Peanut Butter', 'Snack', 200, 6, 24, 12, 4, '1 apple'),
    ('Mixed Nuts', 'Snack', 180, 5, 8, 16, 2, '30g'),
    ('Protein Bar', 'Snack', 220, 20, 22, 8, 3, '1 bar'),
    ('Cheese and Crackers', 'Snack', 180, 8, 15, 10, 1, '1 serving'),
    ('Celery with Almond Butter', 'Snack', 150, 4, 8, 12, 3, '3 stalks'),
    ('Trail Mix', 'Snack', 200, 6, 22, 12, 3, '40g'),
    ('Rice Cakes with Avocado', 'Snack', 160, 4, 18, 8, 4, '2 cakes'),
    ('Dark Chocolate', 'Snack', 170, 2, 18, 12, 3, '30g'),
    ('Edamame', 'Snack', 120, 12, 10, 5, 5, '1 cup'),
    ('Carrot Sticks with Hummus', 'Snack', 140, 5, 18, 6, 5, '1 serving'),
    ('Popcorn', 'Snack', 110, 3, 22, 2, 4, '3 cups'),
    ('String Cheese', 'Snack', 80, 7, 1, 5, 0, '1 stick'),
    ('Beef Jerky', 'Snack', 120, 20, 4, 2, 0, '30g'),
    ('Roasted Chickpeas', 'Snack', 140, 6, 22, 3, 6, '1/2 cup'),
    ('Frozen Yogurt', 'Snack', 150, 4, 28, 3, 0, '1/2 cup'),
    ('Energy Balls', 'Snack', 180, 5, 22, 10, 3, '2 balls'),
    ('Guacamole with Chips', 'Snack', 220, 3, 22, 14, 5, '1 serving'),
    ('Dried Mango', 'Snack', 160, 1, 38, 0, 3, '40g'),
    ('Cucumber Slices with Tzatziki', 'Snack', 80, 3, 8, 4, 2, '1 cup'),
    ('Banana with Nutella', 'Snack', 250, 4, 45, 8, 4, '1 banana'),
    
    # Beverages (15)
    ('Green Smoothie', 'Beverage', 180, 6, 32, 4, 5, '1 glass'),
    ('Protein Shake', 'Beverage', 220, 30, 12, 5, 2, '1 glass'),
    ('Fresh Orange Juice', 'Beverage', 120, 2, 28, 0, 1, '1 glass'),
    ('Iced Coffee', 'Beverage', 80, 1, 12, 3, 0, '1 glass'),
    ('Matcha Latte', 'Beverage', 150, 5, 18, 6, 1, '1 cup'),
    ('Berry Smoothie', 'Beverage', 200, 8, 38, 3, 4, '1 glass'),
    ('Coconut Water', 'Beverage', 50, 1, 12, 0, 0, '1 cup'),
    ('Hot Chocolate', 'Beverage', 180, 8, 28, 5, 2, '1 cup'),
    ('Mango Lassi', 'Beverage', 200, 6, 35, 4, 2, '1 glass'),
    ('Chai Latte', 'Beverage', 150, 4, 25, 4, 0, '1 cup'),
    ('Vegetable Juice', 'Beverage', 70, 2, 15, 0, 2, '1 glass'),
    ('Almond Milk Smoothie', 'Beverage', 160, 5, 25, 6, 3, '1 glass'),
    ('Iced Green Tea', 'Beverage', 30, 0, 8, 0, 0, '1 glass'),
    ('Strawberry Banana Shake', 'Beverage', 220, 8, 42, 4, 3, '1 glass'),
    ('Golden Milk', 'Beverage', 130, 4, 15, 6, 1, '1 cup'),
]

for meal in meals:
    try:
        cursor.execute("""INSERT INTO MEALS (meal_name, meal_category, calories, protein, carbohydrates, fats, fiber, serving_size) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", meal)
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass
conn.commit()
print(f"   ✓ Inserted {len(meals)} unique meals")

# Step 3: Insert UNIQUE ACTIVITIES (60+ unique activities)
print("\n[3/4] Inserting activities...")
activities = [
    # Cardio (20)
    ('Running', 'Cardio', 11.0, 'High'),
    ('Jogging', 'Cardio', 8.0, 'Moderate'),
    ('Sprinting', 'Cardio', 15.0, 'Very High'),
    ('Walking', 'Cardio', 4.0, 'Low'),
    ('Power Walking', 'Cardio', 6.0, 'Moderate'),
    ('Hiking', 'Cardio', 7.0, 'Moderate'),
    ('Stair Climbing', 'Cardio', 9.0, 'High'),
    ('Cycling', 'Cardio', 8.0, 'Moderate'),
    ('Mountain Biking', 'Cardio', 10.0, 'High'),
    ('Stationary Bike', 'Cardio', 7.0, 'Moderate'),
    ('Swimming', 'Cardio', 9.0, 'High'),
    ('Rowing', 'Cardio', 8.5, 'High'),
    ('Elliptical Trainer', 'Cardio', 8.0, 'Moderate'),
    ('Jump Rope', 'Cardio', 12.0, 'Very High'),
    ('Kickboxing', 'Cardio', 10.0, 'High'),
    ('Aerobics', 'Cardio', 7.5, 'Moderate'),
    ('Zumba', 'Cardio', 8.0, 'High'),
    ('Dancing', 'Cardio', 6.5, 'Moderate'),
    ('Step Aerobics', 'Cardio', 8.5, 'High'),
    ('Spinning Class', 'Cardio', 10.0, 'High'),
    
    # Strength Training (15)
    ('Weight Lifting', 'Strength', 5.0, 'Moderate'),
    ('Deadlifts', 'Strength', 6.0, 'High'),
    ('Bench Press', 'Strength', 5.5, 'Moderate'),
    ('Squats', 'Strength', 6.0, 'High'),
    ('Lunges', 'Strength', 5.0, 'Moderate'),
    ('Push-ups', 'Strength', 4.5, 'Moderate'),
    ('Pull-ups', 'Strength', 5.0, 'High'),
    ('Dumbbell Curls', 'Strength', 4.0, 'Low'),
    ('Kettlebell Swings', 'Strength', 8.0, 'High'),
    ('Resistance Bands', 'Strength', 4.0, 'Low'),
    ('Leg Press', 'Strength', 5.0, 'Moderate'),
    ('Shoulder Press', 'Strength', 4.5, 'Moderate'),
    ('Tricep Dips', 'Strength', 4.0, 'Moderate'),
    ('Cable Exercises', 'Strength', 4.5, 'Moderate'),
    ('Barbell Rows', 'Strength', 5.5, 'Moderate'),
    
    # Flexibility & Balance (10)
    ('Yoga', 'Flexibility', 3.5, 'Low'),
    ('Pilates', 'Flexibility', 4.0, 'Moderate'),
    ('Stretching', 'Flexibility', 2.5, 'Low'),
    ('Tai Chi', 'Flexibility', 3.0, 'Low'),
    ('Barre Workout', 'Flexibility', 5.0, 'Moderate'),
    ('Hot Yoga', 'Flexibility', 5.5, 'Moderate'),
    ('Foam Rolling', 'Flexibility', 2.0, 'Low'),
    ('Balance Training', 'Flexibility', 3.0, 'Low'),
    ('Dynamic Stretching', 'Flexibility', 3.5, 'Low'),
    ('Mobility Exercises', 'Flexibility', 3.0, 'Low'),
    
    # Sports (15)
    ('Basketball', 'Sports', 9.0, 'High'),
    ('Soccer', 'Sports', 10.0, 'High'),
    ('Tennis', 'Sports', 8.0, 'High'),
    ('Badminton', 'Sports', 6.5, 'Moderate'),
    ('Volleyball', 'Sports', 5.0, 'Moderate'),
    ('Table Tennis', 'Sports', 4.0, 'Moderate'),
    ('Golf', 'Sports', 3.5, 'Low'),
    ('Baseball', 'Sports', 5.0, 'Moderate'),
    ('Hockey', 'Sports', 9.0, 'High'),
    ('Rugby', 'Sports', 10.0, 'Very High'),
    ('Boxing', 'Sports', 11.0, 'Very High'),
    ('Wrestling', 'Sports', 9.0, 'High'),
    ('Martial Arts', 'Sports', 8.0, 'High'),
    ('Handball', 'Sports', 9.0, 'High'),
    ('Squash', 'Sports', 10.0, 'High'),
    
    # HIIT & Functional (10)
    ('CrossFit', 'HIIT', 12.0, 'Very High'),
    ('Burpees', 'HIIT', 10.0, 'High'),
    ('Box Jumps', 'HIIT', 9.0, 'High'),
    ('Battle Ropes', 'HIIT', 10.5, 'Very High'),
    ('Circuit Training', 'HIIT', 9.0, 'High'),
    ('Tabata Workout', 'HIIT', 11.0, 'Very High'),
    ('Plyometrics', 'HIIT', 10.0, 'High'),
    ('Agility Ladder', 'HIIT', 8.0, 'High'),
    ('Medicine Ball Exercises', 'HIIT', 7.0, 'Moderate'),
    ('Sled Push', 'HIIT', 11.0, 'Very High'),
]

for activity in activities:
    try:
        cursor.execute("""INSERT INTO ACTIVITIES (activity_name, activity_category, calories_per_minute, intensity_level) 
                         VALUES (%s, %s, %s, %s)""", activity)
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass
conn.commit()
print(f"   ✓ Inserted {len(activities)} unique activities")

# Step 4: Insert sample users and logs
print("\n[4/4] Inserting sample users and logs...")

# Create 30 realistic users
first_names = ['James', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'William', 'Sophia', 'Benjamin', 'Isabella',
               'Lucas', 'Mia', 'Henry', 'Charlotte', 'Alexander', 'Amelia', 'Michael', 'Harper', 'Daniel', 'Evelyn',
               'Matthew', 'Abigail', 'Joseph', 'Emily', 'David', 'Elizabeth', 'Samuel', 'Sofia', 'Sebastian', 'Victoria']
last_names = ['Anderson', 'Thompson', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall',
              'Allen', 'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams',
              'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell']

user_ids = []
for i in range(30):
    fn, ln = first_names[i], last_names[i]
    try:
        cursor.execute("""INSERT INTO USERS (username, email, password_hash, first_name, last_name, gender, 
                         date_of_birth, weight, height, activity_level) 
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                      (f'{fn.lower()}.{ln.lower()}', f'{fn.lower()}.{ln.lower()}@email.com', 'password123',
                       fn, ln, random.choice(['Male', 'Female']),
                       datetime(1985, 1, 1) + timedelta(days=random.randint(0, 10000)),
                       round(random.uniform(55.0, 95.0), 1), round(random.uniform(155.0, 190.0), 1),
                       random.choice(['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'])))
        conn.commit()
        cursor.execute("SELECT user_id FROM USERS WHERE username = %s", (f'{fn.lower()}.{ln.lower()}',))
        result = cursor.fetchone()
        if result:
            user_ids.append(result[0])
    except Exception as e:
        conn.rollback()
        pass

print(f"   ✓ Created {len(user_ids)} users")

# Create goals for users
for uid in user_ids[:20]:
    try:
        cursor.execute("""INSERT INTO GOALS (user_id, goal_type, target_value, current_value, start_date, target_date, status) 
                         VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                      (uid, random.choice(['Weight Loss', 'Weight Gain', 'Maintain Weight', 'Muscle Gain']),
                       round(random.uniform(60.0, 80.0), 1), round(random.uniform(65.0, 90.0), 1),
                       datetime.now() - timedelta(days=random.randint(10, 30)),
                       datetime.now() + timedelta(days=random.randint(30, 90)), 'Active'))
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass
print("   ✓ Created goals")

# Create daily logs
daily_log_ids = []
for uid in user_ids:
    for day_offset in range(random.randint(5, 15)):
        try:
            cursor.execute("""INSERT INTO DAILY_LOG (user_id, log_date, total_calories_consumed, total_calories_burned, 
                             water_intake, sleep_hours, weight, notes) 
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                          (uid, datetime.now() - timedelta(days=day_offset),
                           round(random.uniform(1600.0, 2800.0), 0), round(random.uniform(200.0, 700.0), 0),
                           round(random.uniform(5.0, 10.0), 1), round(random.uniform(5.5, 9.0), 1),
                           round(random.uniform(58.0, 95.0), 1),
                           random.choice(['Feeling great', 'Good day', 'Productive', 'Tired but happy', 'Normal day', ''])))
            conn.commit()
        except Exception as e:
            conn.rollback()
            pass

cursor.execute("SELECT daily_log_id FROM DAILY_LOG")
daily_log_ids = [row[0] for row in cursor.fetchall()]
print(f"   ✓ Created {len(daily_log_ids)} daily logs")

# Get meal and activity IDs
cursor.execute("SELECT meal_id FROM MEALS")
meal_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT activity_id FROM ACTIVITIES")
activity_ids = [row[0] for row in cursor.fetchall()]

# Create meal logs
for _ in range(200):
    try:
        cursor.execute("""INSERT INTO MEAL_LOG (daily_log_id, meal_id, quantity, total_calories, notes) 
                         VALUES (%s,%s,%s,%s,%s)""",
                      (random.choice(daily_log_ids), random.choice(meal_ids),
                       round(random.uniform(0.5, 2.0), 1), round(random.uniform(150.0, 600.0), 0),
                       random.choice(['Delicious', 'Healthy', 'Quick meal', 'Homemade', ''])))
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass
print("   ✓ Created meal logs")

# Create activity logs
for _ in range(150):
    try:
        cursor.execute("""INSERT INTO ACTIVITY_LOG (daily_log_id, activity_id, duration_minutes, calories_burned, notes) 
                         VALUES (%s,%s,%s,%s,%s)""",
                      (random.choice(daily_log_ids), random.choice(activity_ids),
                       random.randint(15, 90), round(random.uniform(100.0, 600.0), 0),
                       random.choice(['Great workout', 'Felt strong', 'Challenging', 'Morning session', ''])))
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass
print("   ✓ Created activity logs")

# Create mood logs
for _ in range(100):
    try:
        cursor.execute("""INSERT INTO MOOD_LOG (daily_log_id, mood_rating, stress_level, energy_level, notes) 
                         VALUES (%s,%s,%s,%s,%s)""",
                      (random.choice(daily_log_ids), random.randint(3, 5),
                       random.choice(['Low', 'Moderate', 'High']),
                       random.choice(['Low', 'Moderate', 'High']),
                       random.choice(['Feeling positive', 'Relaxed', 'Motivated', 'Happy', ''])))
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass
print("   ✓ Created mood logs")

cursor.close()
conn.close()

print("\n" + "=" * 50)
print("✅ DATABASE SETUP COMPLETE!")
print("=" * 50)
print(f"""
Summary:
- {len(meals)} unique meals (Breakfast, Lunch, Dinner, Snack, Beverage)
- {len(activities)} unique activities (Cardio, Strength, Flexibility, Sports, HIIT)
- 30 sample users with realistic names
- Goals, daily logs, meal logs, activity logs, and mood logs

All entries have UNIQUE names - no duplicates!
""")
