"""
================================================================================
                     SMART DIET PLANNER - AI ENGINE
                        VIVA DEMONSTRATION MODULE
================================================================================

This module demonstrates 6 Classical AI Concepts from our lab syllabus:

1. AI AGENT (Lab 2-3)
   - Definition: An entity that perceives its environment and takes actions
   - Our Implementation: DietPlannerAgent class
   - Frontend: User submits goal → Agent perceives data → Agent decides → Shows recommendation

2. STATE SPACE SEARCH + BFS (Lab 4-5)
   - Definition: Exploring possible states to find a solution path
   - Our Implementation: Search through meal categories to find matching foods
   - Frontend: Shows recommended foods searched from database

3. A* SEARCH (Lab 7)
   - Definition: Best-first search using f(n) = g(n) + h(n)
   - Our Implementation: Find optimal meal plan considering calories + nutrition score
   - Frontend: Shows "optimal" food choices ranked by both cost and benefit

4. DEDUCTIVE REASONING (Lab 8)
   - Definition: General rules → Specific conclusions
   - Our Implementation: IF goal=lose_weight AND calories>2000 THEN reduce_calories
   - Frontend: Shows reasoning chain "Based on your goal, we recommend..."

5. FUZZY LOGIC (Lab 10)
   - Definition: Degrees of truth instead of binary true/false
   - Our Implementation: Calorie intake is "LOW", "MEDIUM", or "HIGH" with membership degrees
   - Frontend: Shows fuzzy evaluation like "Your calorie intake is 70% high"

6. CONDITIONAL PROBABILITY (Lab 11)
   - Definition: P(A|B) = Probability of A given B has occurred
   - Our Implementation: P(weight_gain | high_calories, low_activity)
   - Frontend: Shows risk percentage "Based on patterns, 75% chance of weight gain"

================================================================================
FRONTEND CONNECTIONS:
================================================================================
- User Dashboard → "AI Recommendations" page → Form with goal selection
- User clicks "Get AI Recommendation" → This module runs
- Result shows: Main Recommendation, Reasoning, Food List, Activity List, Risk %
- History saved in SUGGESTIONS table → Viewable in "AI History" page

================================================================================
"""

import psycopg2
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================================
#                           DATABASE CONNECTION
# ============================================================================

def _to_pg(query, params):
    """Convert Oracle :name params to psycopg2 %(name)s params."""
    if params and isinstance(params, dict):
        return re.sub(r':([a-zA-Z_]\w*)', r'%(\1)s', query), params
    return query, params


def get_connection():
    """Create database connection"""
    return psycopg2.connect(
        host=os.getenv("PG_HOST",     "localhost"),
        port=os.getenv("PG_PORT",     "5432"),
        database=os.getenv("PG_DATABASE", "smart_diet_planner"),
        user=os.getenv("PG_USER",     "postgres"),
        password=os.getenv("PG_PASSWORD", "postgres")
    )


def execute_query(query, params=None, fetch=True):
    """Execute a database query and return results"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if params:
            q, p = _to_pg(query, params)
            cursor.execute(q, p)
        else:
            cursor.execute(query)

        if fetch:
            columns = [col[0].lower() for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
        else:
            conn.commit()
            result = True

        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"❌ Database error: {e}")
        return [] if fetch else False


# ============================================================================
#                    CONCEPT 1: AI AGENT (Lab 2-3)
# ============================================================================
"""
AI AGENT CONCEPT:
- An agent PERCEIVES its environment through sensors
- The agent THINKS/DECIDES based on perceived information
- The agent ACTS based on its decision

In our system:
- PERCEIVE: Gather user data (logs, meals, activities, mood)
- DECIDE: Apply AI techniques to find best recommendation
- ACT: Return recommendation to user
"""

class DietPlannerAgent:
    """
    An AI Agent for diet planning.
    
    This class demonstrates the AGENT concept from Lab 2-3:
    - perceive(): Collect data from environment (database)
    - decide(): Use AI techniques to make a decision
    - act(): Return the recommendation to user
    """
    
    def __init__(self, user_id, goal):
        """Initialize agent with user context"""
        self.user_id = user_id
        self.goal = goal  # 'lose', 'gain', or 'maintain'
        
        # Agent's knowledge base (will be filled during perception)
        self.user_profile = None
        self.daily_logs = []
        self.meal_logs = []
        self.activity_logs = []
        self.mood_logs = []
        
        # Reasoning results (will be filled during decision)
        self.deductive_result = None
        self.fuzzy_result = None
        self.probability_result = None
        self.search_result = None
    
    # -------------------------------------------------------------------------
    # PERCEIVE: Gather information from environment
    # -------------------------------------------------------------------------
    def perceive(self):
        """
        PERCEPTION PHASE of the agent.
        Gathers all relevant data from the database about the user.
        
        This is like the agent's "sensors" collecting information.
        """
        print(f"🔍 Agent PERCEIVING environment for user {self.user_id}...")
        
        # Get user profile
        self.user_profile = self._get_user_profile()
        
        # Get recent logs (last 14 days)
        self.daily_logs = self._get_daily_logs()
        self.meal_logs = self._get_meal_logs()
        self.activity_logs = self._get_activity_logs()
        self.mood_logs = self._get_mood_logs()
        
        print(f"   ✅ Perceived: {len(self.daily_logs)} daily logs, "
            f"{len(self.meal_logs)} meals, {len(self.activity_logs)} activities")
        
        return True
    
    def _get_user_profile(self):
        """Get user's basic profile information"""
        # Columns: USER_ID, USERNAME, EMAIL, GENDER, WEIGHT, HEIGHT, ACTIVITY_LEVEL, DIETARY_PREFERENCE
        query = """
            SELECT user_id, username, email, gender, height, weight, 
                   activity_level, dietary_preference
            FROM USERS WHERE user_id = :user_id
        """
        result = execute_query(query, {'user_id': self.user_id})
        return result[0] if result else {}
    
    def _get_daily_logs(self):
        """Get user's daily logs from last 14 days"""
        # Table: DAILY_LOG (not DAILY_LOGS)
        # Columns: DAILY_LOG_ID, USER_ID, LOG_DATE, TOTAL_CALORIES_CONSUMED, WATER_INTAKE, SLEEP_HOURS
        query = """
            SELECT daily_log_id, log_date,
                   COALESCE(total_calories_consumed, 0) as total_calories,
                   COALESCE(water_intake, 0) as water_intake,
                   COALESCE(sleep_hours, 7) as sleep_hours
            FROM DAILY_LOG
            WHERE user_id = :user_id
            AND log_date >= CURRENT_DATE - 14
            ORDER BY log_date DESC
        """
        return execute_query(query, {'user_id': self.user_id})
    
    def _get_meal_logs(self):
        """Get user's meal logs from last 14 days"""
        # MEAL_LOG: MEAL_LOG_ID, DAILY_LOG_ID, MEAL_ID, MEAL_TIME, QUANTITY, TOTAL_CALORIES
        # MEALS: MEAL_ID, MEAL_NAME, MEAL_CATEGORY, CALORIES, PROTEIN, CARBOHYDRATES, FATS
        query = """
            SELECT ml.meal_log_id, m.meal_name, m.meal_category, 
                   ml.total_calories, m.protein, m.carbohydrates, m.fats,
                   d.log_date
            FROM MEAL_LOG ml
            JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
            JOIN MEALS m ON ml.meal_id = m.meal_id
            WHERE d.user_id = :user_id
            AND d.log_date >= CURRENT_DATE - 14
        """
        return execute_query(query, {'user_id': self.user_id})
    
    def _get_activity_logs(self):
        """Get user's activity logs from last 14 days"""
        # ACTIVITY_LOG: ACTIVITY_LOG_ID, DAILY_LOG_ID, ACTIVITY_ID, DURATION_MINUTES, CALORIES_BURNED
        query = """
            SELECT a.activity_log_id, a.duration_minutes, a.calories_burned, d.log_date
            FROM ACTIVITY_LOG a
            JOIN DAILY_LOG d ON a.daily_log_id = d.daily_log_id
            WHERE d.user_id = :user_id
            AND d.log_date >= CURRENT_DATE - 14
        """
        return execute_query(query, {'user_id': self.user_id})
    
    def _get_mood_logs(self):
        """Get user's mood/energy patterns"""
        # MOOD_LOG: MOOD_LOG_ID, DAILY_LOG_ID, MOOD_RATING, STRESS_LEVEL, ENERGY_LEVEL
        query = """
            SELECT m.mood_rating, m.stress_level, m.energy_level, d.log_date
            FROM MOOD_LOG m
            JOIN DAILY_LOG d ON m.daily_log_id = d.daily_log_id
            WHERE d.user_id = :user_id
            AND d.log_date >= CURRENT_DATE - 14
        """
        return execute_query(query, {'user_id': self.user_id})
    
    # -------------------------------------------------------------------------
    # DECIDE: Apply AI techniques to make a decision
    # -------------------------------------------------------------------------
    def decide(self):
        """
        DECISION PHASE of the agent.
        Applies multiple AI techniques to generate a recommendation.
        
        Uses:
        - Deductive Reasoning (rules → conclusions)
        - Fuzzy Logic (degree of membership)
        - Conditional Probability (risk assessment)
        - Search (find best foods)
        """
        print(f"🧠 Agent DECIDING (applying AI techniques)...")
        
        # Apply AI techniques
        self.deductive_result = self._apply_deductive_reasoning()
        self.fuzzy_result = self._apply_fuzzy_logic()
        self.probability_result = self._calculate_probability()
        self.search_result = self._search_optimal_foods()
        
        print(f"   ✅ Decision complete!")
        return True
    
    # -------------------------------------------------------------------------
    # ACT: Return the recommendation
    # -------------------------------------------------------------------------
    def act(self):
        """
        ACTION PHASE of the agent.
        Compiles all analysis into a final recommendation.
        
        Returns a dictionary with:
        - success: bool
        - recommendation: main advice text
        - explanation: reasoning explanation
        - food_recommendations: list of foods
        - activity_recommendations: list of activities
        - risk_assessment: probability results
        - fuzzy_evaluation: fuzzy logic results
        """
        print(f"🎯 Agent ACTING (generating recommendation)...")
        
        result = {
            'success': True,
            'recommendation': self._generate_main_recommendation(),
            'explanation': self._generate_explanation(),
            'food_recommendations': self.search_result.get('foods', []),
            'activity_recommendations': self._get_activity_suggestions(),
            'risk_assessment': self.probability_result,
            'fuzzy_evaluation': self.fuzzy_result,
            'ai_confidence': self._calculate_confidence()
        }
        
        print(f"   ✅ Action complete! Recommendation ready.")
        return result


# ============================================================================
#                 CONCEPT 2 & 3: STATE SPACE SEARCH & A* (Lab 4-7)
# ============================================================================
"""
STATE SPACE SEARCH CONCEPT:
- Problem represented as states and transitions
- Start state → Goal state through a path
- BFS: Explore level by level (queue)
- DFS: Explore depth first (stack)

A* SEARCH CONCEPT:
- Best-first search using: f(n) = g(n) + h(n)
- g(n) = cost from start to current node
- h(n) = heuristic estimate to goal
- Always expands node with lowest f(n)

In our diet planner:
- States = Different food combinations
- Goal = Optimal calorie/nutrition balance
- g(n) = Calories (cost)
- h(n) = Nutrition score (benefit estimate)
"""

class FoodSearchEngine:
    """
    Implements STATE SPACE SEARCH and A* concepts for finding optimal foods.
    
    - BFS: Search through food categories level by level
    - A*: Rank foods by f(n) = calorie_cost + nutrition_benefit
    """
    
    def __init__(self, goal, target_calories=2000):
        self.goal = goal
        self.target_calories = target_calories
    
    def bfs_search_categories(self):
        r"""
        BFS SEARCH: Find food categories that match the goal.
        
        Search Tree:
                        [All Foods]
                       /    |    \
               [Proteins] [Carbs] [Fats]
               /    \       |       \
          [Chicken][Fish] [Rice]   [Nuts]
        
        BFS explores level by level using a queue.
        """
        print("   🔎 Running BFS to search food categories...")
        
        # Define the search tree (categories → subcategories → foods)
        search_tree = {
            'All Foods': ['Proteins', 'Carbs', 'Healthy Fats', 'Vegetables'],
            'Proteins': ['Meat', 'Fish', 'Eggs', 'Legumes'],
            'Carbs': ['Grains', 'Fruits', 'Starchy Vegetables'],
            'Healthy Fats': ['Nuts', 'Seeds', 'Oils'],
            'Vegetables': ['Leafy Greens', 'Cruciferous', 'Root Vegetables']
        }
        
        # BFS using a queue (FIFO)
        queue = ['All Foods']  # Start state
        visited = []
        path = []
        
        while queue:
            current = queue.pop(0)  # Dequeue (FIFO)
            if current not in visited:
                visited.append(current)
                path.append(current)
                
                # Add children to queue
                if current in search_tree:
                    for child in search_tree[current]:
                        queue.append(child)
        
        print(f"   ✅ BFS visited: {' → '.join(path[:5])}...")
        return path
    
    def a_star_rank_foods(self, foods_from_db):
        """
        A* SEARCH: Rank foods by f(n) = g(n) + h(n)
        
        - g(n) = Calorie cost (lower is better for weight loss)
        - h(n) = Nutrition score heuristic (higher is better)
        - f(n) = Combined score (we want to MINIMIZE this)
        
        For weight loss: prioritize low calorie, high nutrition
        For weight gain: prioritize high calorie, high nutrition
        """
        print("   🔎 Running A* to rank foods optimally...")
        
        ranked_foods = []
        
        for food in foods_from_db:
            name = food.get('food_name', 'Unknown')
            calories = food.get('calories_per_serving', 100)
            protein = food.get('protein', 0)
            fiber = food.get('fiber', 0)
            
            # g(n) = calorie cost (normalize to 0-1 scale)
            g_n = calories / 500  # Normalize: 500 cal = 1.0
            
            # h(n) = nutrition heuristic (higher protein and fiber = better)
            # We invert it since A* minimizes f(n)
            nutrition_score = (protein * 2 + fiber) / 50  # Normalize
            h_n = 1 - min(nutrition_score, 1)  # Invert: good nutrition = low h(n)
            
            # f(n) = g(n) + h(n)
            if self.goal == 'lose':
                # For weight loss: prioritize LOW calories, HIGH nutrition
                f_n = g_n + h_n
            elif self.goal == 'gain':
                # For weight gain: prioritize HIGH calories, HIGH nutrition
                f_n = (1 - g_n) + h_n  # Invert calorie cost
            else:
                # For maintenance: balance both
                f_n = abs(g_n - 0.5) + h_n
            
            ranked_foods.append({
                'name': name,
                'calories': calories,
                'protein': protein,
                'g_n': round(g_n, 2),
                'h_n': round(h_n, 2),
                'f_n': round(f_n, 2)
            })
        
        # Sort by f(n) - A* always expands lowest f(n) first
        ranked_foods.sort(key=lambda x: x['f_n'])
        
        print(f"   ✅ A* ranked {len(ranked_foods)} foods by f(n)")
        return ranked_foods[:10]  # Return top 10


# ============================================================================
#                  CONCEPT 4: DEDUCTIVE REASONING (Lab 8)
# ============================================================================
"""
DEDUCTIVE REASONING CONCEPT:
- Start with general rules (premises)
- Apply to specific situation
- Derive specific conclusion

Example:
- Rule 1: IF goal = "lose weight" THEN target_calories < current_calories
- Rule 2: IF calories_consumed > 2000 THEN status = "high"
- Rule 3: IF status = "high" AND goal = "lose" THEN action = "reduce calories"

In our system:
- We have diet rules in our knowledge base
- We apply them to user's specific data
- We derive specific recommendations
"""

class DeductiveReasoner:
    """
    Implements DEDUCTIVE REASONING for diet recommendations.
    
    Uses IF-THEN rules to derive conclusions from general principles.
    """
    
    def __init__(self):
        # Knowledge Base: General rules about diet
        self.rules = [
            # Rule format: (conditions, conclusion)
            {
                'id': 'R1',
                'conditions': {'goal': 'lose', 'calorie_status': 'high'},
                'conclusion': 'reduce_calories',
                'explanation': 'You want to lose weight and your calorie intake is high, so reduce calories.'
            },
            {
                'id': 'R2', 
                'conditions': {'goal': 'lose', 'protein_status': 'low'},
                'conclusion': 'increase_protein',
                'explanation': 'For weight loss, you need more protein to preserve muscle. Increase protein intake.'
            },
            {
                'id': 'R3',
                'conditions': {'goal': 'gain', 'calorie_status': 'low'},
                'conclusion': 'increase_calories',
                'explanation': 'You want to gain weight but your calorie intake is low. Eat more calories.'
            },
            {
                'id': 'R4',
                'conditions': {'goal': 'gain', 'protein_status': 'low'},
                'conclusion': 'increase_protein',
                'explanation': 'For muscle gain, you need high protein. Increase protein-rich foods.'
            },
            {
                'id': 'R5',
                'conditions': {'activity_status': 'low'},
                'conclusion': 'increase_activity',
                'explanation': 'Your physical activity is low. Try to be more active for better health.'
            },
            {
                'id': 'R6',
                'conditions': {'mood_status': 'low', 'sleep_status': 'low'},
                'conclusion': 'improve_sleep',
                'explanation': 'Low mood combined with poor sleep. Better sleep will improve your mood.'
            },
            {
                'id': 'R7',
                'conditions': {'goal': 'maintain', 'calorie_status': 'balanced'},
                'conclusion': 'maintain_current',
                'explanation': 'Your calorie balance is good for maintenance. Keep up the good work!'
            }
        ]
    
    def evaluate_status(self, avg_calories, avg_protein, avg_activity, avg_mood, avg_sleep, goal):
        """Evaluate user's current status based on their data"""
        
        status = {}
        
        # Calorie status
        if goal == 'lose':
            target = 1800
        elif goal == 'gain':
            target = 2500
        else:
            target = 2000
        
        if avg_calories > target * 1.1:
            status['calorie_status'] = 'high'
        elif avg_calories < target * 0.9:
            status['calorie_status'] = 'low'
        else:
            status['calorie_status'] = 'balanced'
        
        # Protein status
        if avg_protein < 50:
            status['protein_status'] = 'low'
        elif avg_protein > 100:
            status['protein_status'] = 'high'
        else:
            status['protein_status'] = 'adequate'
        
        # Activity status
        if avg_activity < 30:
            status['activity_status'] = 'low'
        else:
            status['activity_status'] = 'adequate'
        
        # Mood status
        if avg_mood and avg_mood < 5:
            status['mood_status'] = 'low'
        else:
            status['mood_status'] = 'ok'
        
        # Sleep status
        if avg_sleep and avg_sleep < 6:
            status['sleep_status'] = 'low'
        else:
            status['sleep_status'] = 'ok'
        
        status['goal'] = goal
        return status
    
    def apply_rules(self, status):
        """
        DEDUCTIVE REASONING: Apply rules to derive conclusions.
        
        For each rule, check if ALL conditions match.
        If yes, the rule "fires" and we get a conclusion.
        """
        print("   📜 Applying deductive reasoning rules...")
        
        fired_rules = []
        conclusions = []
        
        for rule in self.rules:
            # Check if all conditions in the rule are satisfied
            conditions_met = True
            for key, value in rule['conditions'].items():
                if status.get(key) != value:
                    conditions_met = False
                    break
            
            if conditions_met:
                # Rule fires!
                fired_rules.append(rule['id'])
                conclusions.append({
                    'rule': rule['id'],
                    'action': rule['conclusion'],
                    'explanation': rule['explanation']
                })
                print(f"      ✓ Rule {rule['id']} fired: {rule['conclusion']}")
        
        if not fired_rules:
            print("      ℹ️ No specific rules fired, using default recommendations")
            conclusions.append({
                'rule': 'DEFAULT',
                'action': 'balanced_diet',
                'explanation': 'Maintain a balanced diet with variety.'
            })
        
        return conclusions


# ============================================================================
#                   CONCEPT 5: FUZZY LOGIC (Lab 10)
# ============================================================================
"""
FUZZY LOGIC CONCEPT:
- Traditional logic: TRUE or FALSE (binary)
- Fuzzy logic: Degree of truth (0 to 1)
- Membership functions define how much something belongs to a category

Example:
- Calories = 1900
- Membership in "LOW" = 0.1 (10% low)
- Membership in "MEDIUM" = 0.8 (80% medium)
- Membership in "HIGH" = 0.1 (10% high)

In our system:
- We evaluate calories, activity, sleep using fuzzy sets
- We combine fuzzy values to get an overall assessment
"""

class FuzzyEvaluator:
    """
    Implements FUZZY LOGIC for evaluating diet metrics.
    
    Uses triangular membership functions to determine
    degree of membership in fuzzy sets (LOW, MEDIUM, HIGH).
    """
    
    def __init__(self):
        # Define fuzzy sets for calories (in terms of daily intake)
        # Format: (low_bound, peak, high_bound)
        self.calorie_sets = {
            'LOW': (0, 1000, 1500),       # Low: peaks at 1000
            'MEDIUM': (1200, 1800, 2200),  # Medium: peaks at 1800
            'HIGH': (2000, 2500, 4000)     # High: peaks at 2500
        }
        
        # Define fuzzy sets for activity (minutes per day)
        self.activity_sets = {
            'LOW': (0, 0, 30),
            'MEDIUM': (20, 45, 60),
            'HIGH': (45, 90, 180)
        }
        
        # Define fuzzy sets for sleep (hours)
        self.sleep_sets = {
            'POOR': (0, 4, 6),
            'ADEQUATE': (5, 7, 8),
            'GOOD': (7, 8, 12)
        }
    
    def triangular_membership(self, value, fuzzy_set):
        r"""
        Calculate membership degree using triangular membership function.
        
        The triangular function is defined by three points:
        - a (left foot): membership starts at 0
        - b (peak): membership is 1
        - c (right foot): membership returns to 0
        
                    1 |       /\
                      |      /  \
                      |     /    \
                    0 |____/______\____
                        a    b    c
        """
        a, b, c = fuzzy_set
        
        if value <= a or value >= c:
            return 0.0
        elif a < value <= b:
            return (value - a) / (b - a)
        else:  # b < value < c
            return (c - value) / (c - b)
    
    def evaluate_calories(self, avg_calories):
        """Evaluate calorie intake using fuzzy logic"""
        result = {}
        for label, fuzzy_set in self.calorie_sets.items():
            membership = self.triangular_membership(avg_calories, fuzzy_set)
            result[label] = round(membership, 2)
        return result
    
    def evaluate_activity(self, avg_activity_minutes):
        """Evaluate activity level using fuzzy logic"""
        result = {}
        for label, fuzzy_set in self.activity_sets.items():
            membership = self.triangular_membership(avg_activity_minutes, fuzzy_set)
            result[label] = round(membership, 2)
        return result
    
    def evaluate_sleep(self, avg_sleep_hours):
        """Evaluate sleep quality using fuzzy logic"""
        result = {}
        for label, fuzzy_set in self.sleep_sets.items():
            membership = self.triangular_membership(avg_sleep_hours, fuzzy_set)
            result[label] = round(membership, 2)
        return result
    
    def get_fuzzy_assessment(self, avg_calories, avg_activity, avg_sleep):
        """
        COMPLETE FUZZY EVALUATION
        
        Returns fuzzy membership degrees for all metrics.
        Frontend shows: "Your calorie intake is 70% MEDIUM, 30% HIGH"
        """
        print("   🎚️ Applying fuzzy logic evaluation...")
        
        calorie_fuzzy = self.evaluate_calories(avg_calories)
        activity_fuzzy = self.evaluate_activity(avg_activity)
        sleep_fuzzy = self.evaluate_sleep(avg_sleep)
        
        # Find dominant category for each
        dominant_calorie = max(calorie_fuzzy, key=calorie_fuzzy.get)
        dominant_activity = max(activity_fuzzy, key=activity_fuzzy.get)
        dominant_sleep = max(sleep_fuzzy, key=sleep_fuzzy.get)
        
        print(f"      Calories: {dominant_calorie} ({calorie_fuzzy[dominant_calorie]*100:.0f}%)")
        print(f"      Activity: {dominant_activity} ({activity_fuzzy[dominant_activity]*100:.0f}%)")
        print(f"      Sleep: {dominant_sleep} ({sleep_fuzzy[dominant_sleep]*100:.0f}%)")
        
        return {
            'calories': {
                'value': avg_calories,
                'membership': calorie_fuzzy,
                'dominant': dominant_calorie,
                'description': f"Your calorie intake is {calorie_fuzzy[dominant_calorie]*100:.0f}% {dominant_calorie}"
            },
            'activity': {
                'value': avg_activity,
                'membership': activity_fuzzy,
                'dominant': dominant_activity,
                'description': f"Your activity level is {activity_fuzzy[dominant_activity]*100:.0f}% {dominant_activity}"
            },
            'sleep': {
                'value': avg_sleep,
                'membership': sleep_fuzzy,
                'dominant': dominant_sleep,
                'description': f"Your sleep quality is {sleep_fuzzy[dominant_sleep]*100:.0f}% {dominant_sleep}"
            }
        }


# ============================================================================
#               CONCEPT 6: CONDITIONAL PROBABILITY (Lab 11)
# ============================================================================
"""
CONDITIONAL PROBABILITY CONCEPT:
- P(A|B) = Probability of A given B has occurred
- Bayes' Theorem: P(A|B) = P(B|A) * P(A) / P(B)

In our system:
- P(weight_gain | high_calories, low_activity)
- We estimate based on common knowledge and user patterns

Example calculation:
- Base risk of weight gain: 30%
- If high calories: multiply by 1.5 → 45%
- If low activity: multiply by 1.3 → 58.5%
- Combined: ~60% risk of weight gain
"""

class ProbabilityCalculator:
    """
    Implements CONDITIONAL PROBABILITY for health risk assessment.
    
    Calculates probability of outcomes given user's current patterns.
    """
    
    def __init__(self):
        # Base probabilities (prior probabilities)
        self.base_probabilities = {
            'weight_gain': 0.30,    # 30% base risk
            'weight_loss': 0.30,    # 30% base chance
            'health_risk': 0.20,    # 20% base health risk
            'energy_drop': 0.25     # 25% base risk of low energy
        }
        
        # Conditional multipliers
        # These represent P(condition | outcome) ratios
        self.multipliers = {
            'high_calories': {'weight_gain': 1.5, 'weight_loss': 0.5, 'health_risk': 1.2},
            'low_calories': {'weight_gain': 0.5, 'weight_loss': 1.5, 'energy_drop': 1.3},
            'low_activity': {'weight_gain': 1.3, 'health_risk': 1.4, 'energy_drop': 1.2},
            'high_activity': {'weight_gain': 0.6, 'weight_loss': 1.4, 'health_risk': 0.7},
            'poor_sleep': {'health_risk': 1.3, 'energy_drop': 1.5, 'weight_gain': 1.2},
            'low_protein': {'weight_loss': 0.8, 'energy_drop': 1.2}
        }
    
    def calculate_conditional_probability(self, conditions):
        """
        Calculate conditional probabilities given observed conditions.
        
        P(outcome | conditions) ≈ P(outcome) × Π P(condition_i | outcome) adjustments
        
        This is a simplified Bayesian approach.
        """
        print("   📊 Calculating conditional probabilities...")
        
        results = {}
        
        for outcome, base_prob in self.base_probabilities.items():
            probability = base_prob
            contributing_factors = []
            
            for condition in conditions:
                if condition in self.multipliers:
                    if outcome in self.multipliers[condition]:
                        multiplier = self.multipliers[condition][outcome]
                        probability *= multiplier
                        contributing_factors.append(f"{condition} (×{multiplier})")
            
            # Cap probability at 95%
            probability = min(probability, 0.95)
            
            results[outcome] = {
                'probability': round(probability, 2),
                'percentage': f"{round(probability * 100)}%",
                'factors': contributing_factors
            }
            
            if probability > 0.5:
                print(f"      ⚠️ {outcome}: {probability*100:.0f}% risk")
        
        return results
    
    def assess_risk(self, calorie_status, activity_status, sleep_status, protein_status):
        """
        Assess health risks based on user's current patterns.
        
        Returns probability of various outcomes.
        """
        conditions = []
        
        if calorie_status == 'high':
            conditions.append('high_calories')
        elif calorie_status == 'low':
            conditions.append('low_calories')
        
        if activity_status == 'low':
            conditions.append('low_activity')
        elif activity_status == 'high':
            conditions.append('high_activity')
        
        if sleep_status == 'low':
            conditions.append('poor_sleep')
        
        if protein_status == 'low':
            conditions.append('low_protein')
        
        probabilities = self.calculate_conditional_probability(conditions)
        
        # Generate risk summary
        high_risks = [f"{outcome}: {data['percentage']}" 
                     for outcome, data in probabilities.items() 
                     if data['probability'] > 0.4]
        
        return {
            'conditions': conditions,
            'probabilities': probabilities,
            'high_risks': high_risks,
            'summary': f"Based on your patterns: {', '.join(high_risks)}" if high_risks else "No significant risks detected"
        }


# ============================================================================
#                    INTEGRATE INTO AGENT'S DECIDE METHOD
# ============================================================================

def DietPlannerAgent_apply_deductive_reasoning(self):
    """Apply deductive reasoning using user's data"""
    
    # Calculate averages from logs
    avg_calories = 0
    avg_protein = 0
    avg_activity = 0
    avg_mood = None
    avg_sleep = None
    
    if self.daily_logs:
        calories = [log.get('total_calories', 0) or 0 for log in self.daily_logs]
        proteins = [log.get('total_protein', 0) or 0 for log in self.daily_logs]
        moods = [log.get('mood', 0) for log in self.daily_logs if log.get('mood')]
        sleeps = [log.get('sleep_hours', 0) for log in self.daily_logs if log.get('sleep_hours')]
        
        avg_calories = sum(calories) / len(calories) if calories else 0
        avg_protein = sum(proteins) / len(proteins) if proteins else 0
        avg_mood = sum(moods) / len(moods) if moods else None
        avg_sleep = sum(sleeps) / len(sleeps) if sleeps else None
    
    if self.activity_logs:
        durations = [log.get('duration_minutes', 0) or 0 for log in self.activity_logs]
        avg_activity = sum(durations) / len(self.daily_logs) if self.daily_logs else 0
    
    # Create reasoner and apply rules
    reasoner = DeductiveReasoner()
    status = reasoner.evaluate_status(
        avg_calories, avg_protein, avg_activity, avg_mood, avg_sleep, self.goal
    )
    conclusions = reasoner.apply_rules(status)
    
    self._avg_calories = avg_calories
    self._avg_protein = avg_protein
    self._avg_activity = avg_activity
    self._avg_mood = avg_mood
    self._avg_sleep = avg_sleep or 7
    
    return {
        'status': status,
        'conclusions': conclusions
    }


def DietPlannerAgent_apply_fuzzy_logic(self):
    """Apply fuzzy logic evaluation"""
    fuzzy = FuzzyEvaluator()
    return fuzzy.get_fuzzy_assessment(
        self._avg_calories,
        self._avg_activity,
        self._avg_sleep
    )


def DietPlannerAgent_calculate_probability(self):
    """Calculate conditional probabilities for risks"""
    calc = ProbabilityCalculator()
    
    # Get status from deductive reasoning
    status = self.deductive_result.get('status', {})
    
    return calc.assess_risk(
        status.get('calorie_status', 'balanced'),
        status.get('activity_status', 'adequate'),
        status.get('sleep_status', 'ok'),
        status.get('protein_status', 'adequate')
    )


def DietPlannerAgent_search_optimal_foods(self):
    """Search for optimal foods using BFS and A*"""
    
    # Get foods from database
    # MEALS table: MEAL_ID, MEAL_NAME, MEAL_CATEGORY, CALORIES, PROTEIN, CARBOHYDRATES, FATS, FIBER
    query = """
        SELECT meal_name as food_name, meal_category as food_category, 
               calories as calories_per_serving, protein, 
               carbohydrates, fats, fiber
        FROM MEALS
        WHERE calories > 0
    """
    foods = execute_query(query)
    
    if not foods:
        # Fallback foods if database is empty
        foods = [
            {'food_name': 'Grilled Chicken', 'calories_per_serving': 165, 'protein': 31, 'fiber': 0},
            {'food_name': 'Brown Rice', 'calories_per_serving': 216, 'protein': 5, 'fiber': 3},
            {'food_name': 'Salmon', 'calories_per_serving': 208, 'protein': 20, 'fiber': 0},
            {'food_name': 'Broccoli', 'calories_per_serving': 55, 'protein': 4, 'fiber': 5},
            {'food_name': 'Oatmeal', 'calories_per_serving': 150, 'protein': 5, 'fiber': 4},
        ]
    
    # Use search engine
    search = FoodSearchEngine(self.goal)
    
    # Run BFS to explore categories
    categories = search.bfs_search_categories()
    
    # Run A* to rank foods
    ranked_foods = search.a_star_rank_foods(foods)
    
    return {
        'categories_explored': categories,
        'foods': ranked_foods
    }


def DietPlannerAgent_generate_main_recommendation(self):
    """Generate the main recommendation text"""
    
    goal_text = {
        'lose': 'weight loss',
        'gain': 'weight gain',
        'maintain': 'weight maintenance'
    }.get(self.goal, 'healthy eating')
    
    conclusions = self.deductive_result.get('conclusions', [])
    main_actions = [c['action'] for c in conclusions]
    
    if 'reduce_calories' in main_actions:
        rec = f"For {goal_text}, focus on reducing your calorie intake. Choose lower-calorie, nutrient-dense foods."
    elif 'increase_calories' in main_actions:
        rec = f"For {goal_text}, you need to eat more calories. Add healthy, calorie-rich foods to your meals."
    elif 'increase_protein' in main_actions:
        rec = f"Increase your protein intake for better {goal_text}. Include more lean meats, fish, eggs, or legumes."
    else:
        rec = f"Maintain your current balanced diet for {goal_text}. Continue making healthy choices."
    
    return rec


def DietPlannerAgent_generate_explanation(self):
    """Generate explanation of how recommendation was derived"""
    
    parts = []
    
    # Deductive reasoning explanation
    conclusions = self.deductive_result.get('conclusions', [])
    if conclusions:
        parts.append("📜 DEDUCTIVE REASONING:")
        for c in conclusions[:2]:
            parts.append(f"   • {c['explanation']}")
    
    # Fuzzy logic explanation
    if self.fuzzy_result:
        parts.append("\n🎚️ FUZZY LOGIC EVALUATION:")
        for metric in ['calories', 'activity', 'sleep']:
            if metric in self.fuzzy_result:
                parts.append(f"   • {self.fuzzy_result[metric]['description']}")
    
    # Probability explanation
    if self.probability_result and self.probability_result.get('high_risks'):
        parts.append("\n📊 RISK ASSESSMENT:")
        parts.append(f"   • {self.probability_result['summary']}")
    
    return '\n'.join(parts)


def DietPlannerAgent_get_activity_suggestions(self):
    """Get activity suggestions based on goal"""
    
    if self.goal == 'lose':
        return [
            {'name': 'Brisk Walking', 'duration': 30, 'calories': 150},
            {'name': 'Swimming', 'duration': 30, 'calories': 200},
            {'name': 'Cycling', 'duration': 30, 'calories': 180}
        ]
    elif self.goal == 'gain':
        return [
            {'name': 'Weight Training', 'duration': 45, 'calories': 200},
            {'name': 'Resistance Training', 'duration': 30, 'calories': 150},
            {'name': 'Light Cardio', 'duration': 20, 'calories': 100}
        ]
    else:
        return [
            {'name': 'Yoga', 'duration': 30, 'calories': 100},
            {'name': 'Walking', 'duration': 30, 'calories': 120},
            {'name': 'Swimming', 'duration': 30, 'calories': 200}
        ]


def DietPlannerAgent_calculate_confidence(self):
    """Calculate confidence score based on available data"""
    
    data_points = 0
    max_points = 4
    
    if self.daily_logs:
        data_points += 1
    if self.meal_logs:
        data_points += 1
    if self.activity_logs:
        data_points += 1
    if self.mood_logs:
        data_points += 1
    
    return round((data_points / max_points) * 100)


# Bind methods to the class
DietPlannerAgent._apply_deductive_reasoning = DietPlannerAgent_apply_deductive_reasoning
DietPlannerAgent._apply_fuzzy_logic = DietPlannerAgent_apply_fuzzy_logic
DietPlannerAgent._calculate_probability = DietPlannerAgent_calculate_probability
DietPlannerAgent._search_optimal_foods = DietPlannerAgent_search_optimal_foods
DietPlannerAgent._generate_main_recommendation = DietPlannerAgent_generate_main_recommendation
DietPlannerAgent._generate_explanation = DietPlannerAgent_generate_explanation
DietPlannerAgent._get_activity_suggestions = DietPlannerAgent_get_activity_suggestions
DietPlannerAgent._calculate_confidence = DietPlannerAgent_calculate_confidence


# ============================================================================
#                         MAIN FUNCTION FOR FLASK
# ============================================================================

def get_ai_recommendation(user_id, goal='maintain'):
    """
    MAIN ENTRY POINT - Called from Flask route
    
    This function:
    1. Creates an AI Agent
    2. Agent PERCEIVES the environment (gets user data)
    3. Agent DECIDES using AI techniques (reasoning, fuzzy, probability, search)
    4. Agent ACTS (returns recommendation)
    
    Frontend Flow:
    - User clicks "Get AI Recommendation" on dashboard
    - Flask route calls this function
    - Result displayed in cards (main rec, foods, activities, risks)
    """
    print("\n" + "=" * 60)
    print("        SMART DIET PLANNER AI ENGINE")
    print("=" * 60)
    print(f"User: {user_id} | Goal: {goal}")
    print("=" * 60 + "\n")
    
    try:
        # CREATE THE AGENT
        agent = DietPlannerAgent(user_id, goal)
        
        # AGENT LIFECYCLE: Perceive → Decide → Act
        agent.perceive()
        agent.decide()
        result = agent.act()
        
        print("\n" + "=" * 60)
        print("   AI RECOMMENDATION COMPLETE!")
        print("=" * 60 + "\n")
        
        return result
        
    except Exception as e:
        print(f"❌ AI Engine Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'recommendation': 'Sorry, we could not generate a recommendation at this time.',
            'explanation': f'Error: {str(e)}'
        }


# ============================================================================
#                            QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("\n🧪 Testing AI Engine...\n")
    
    # Test with user_id 1
    result = get_ai_recommendation(user_id=1, goal='lose')
    
    print("\n📋 RESULT:")
    print(f"   Success: {result.get('success')}")
    print(f"   Recommendation: {result.get('recommendation')}")
    print(f"   Confidence: {result.get('ai_confidence')}%")
    print(f"\n   Explanation:\n{result.get('explanation')}")
    
    print("\n   Foods:")
    for food in result.get('food_recommendations', [])[:5]:
        print(f"      - {food.get('name')} ({food.get('calories')} cal)")
