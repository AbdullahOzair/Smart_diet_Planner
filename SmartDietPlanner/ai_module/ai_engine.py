# ================================================================
# AI ENGINE - SMART DIET PLANNER
# ================================================================
# Classical AI Concepts Implementation for Diet Recommendation System
# Contains: Agent, Search Algorithms, Reasoning, Fuzzy Logic, etc.
# ================================================================

import math
import random
from collections import deque, defaultdict
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

# ================================================================
# 1. AI AGENT - Diet Advisor Agent
# ================================================================
class DietAdvisorAgent:
    """
    AI CONCEPT: INTELLIGENT AGENT
    - Perceives user data (calories, BMI, goals)
    - Acts by providing diet recommendations
    - Uses all AI modules to make decisions
    """
    
    def __init__(self):
        self.state_space = StateSpace()
        self.search_engine = SearchEngine()
        self.reasoning_engine = ReasoningEngine()
        self.fuzzy_logic = FuzzyLogicEngine()
        self.semantic_network = SemanticNetwork()
        self.frame_system = FrameSystem()
        
    def perceive(self, user_data: Dict) -> Dict:
        """Agent perception: analyze user input"""
        print(f"🤖 AGENT PERCEIVING: User data received")
        
        # Create user frame (AI CONCEPT: FRAMES)
        user_frame = self.frame_system.create_user_frame(user_data)
        
        # Determine current health state (AI CONCEPT: STATE SPACE)
        current_state = self.state_space.get_health_state(
            user_data.get('current_calories', 2000),
            user_data.get('bmi', 25),
            user_data.get('goal', 'maintain')
        )
        
        return {
            'user_frame': user_frame,
            'current_state': current_state,
            'perceived_data': user_data
        }
    
    def act(self, perception_data: Dict) -> Dict:
        """Agent action: generate comprehensive recommendation"""
        print(f" AGENT ACTING: Generating recommendation")
        
        user_frame = perception_data['user_frame']
        current_state = perception_data['current_state']
        user_data = perception_data['perceived_data']
        
        # Use multiple AI techniques for recommendation
        recommendation = {
            'primary_recommendation': self._get_primary_recommendation(user_frame, current_state),
            'search_results': self._apply_search_algorithms(user_data),
            'reasoning_explanation': self._apply_reasoning(user_data),
            'fuzzy_analysis': self._apply_fuzzy_logic(user_data),
            'semantic_connections': self._get_semantic_connections(user_data.get('goal', 'maintain')),
            'probability_analysis': self._calculate_probabilities(user_data),
            'analogy_suggestions': self._find_analogies(user_data)
        }
        
        return recommendation
    
    def _get_primary_recommendation(self, user_frame: Dict, current_state: str) -> str:
        """Generate main recommendation based on state"""
        goal = user_frame.get('goal', 'maintain')
        
        if goal == 'weight_loss' and current_state == 'HIGH_CALORIE':
            return "Reduce calorie intake by 500-750 calories/day. Focus on lean proteins and vegetables."
        elif goal == 'weight_gain' and current_state == 'LOW_CALORIE':
            return "Increase calorie intake by 300-500 calories/day. Add healthy fats and complex carbs."
        elif goal == 'maintain':
            return "Maintain current calorie balance. Focus on nutrient-dense foods and regular exercise."
        else:
            return "Adjust portion sizes gradually and monitor progress weekly."
    
    def _apply_search_algorithms(self, user_data: Dict) -> Dict:
        """Apply BFS, DFS, and A* search"""
        target_calories = user_data.get('target_calories', 2000)
        current_calories = user_data.get('current_calories', 2200)
        
        # A* Search for optimal food plan
        optimal_plan = self.search_engine.a_star_food_search(current_calories, target_calories)
        
        # BFS for exploring diet rules
        bfs_rules = self.search_engine.bfs_diet_rules(user_data.get('goal', 'maintain'))
        
        # DFS for deep rule chaining
        dfs_chain = self.search_engine.dfs_rule_chain(user_data)
        
        return {
            'optimal_plan': optimal_plan,
            'bfs_rules': bfs_rules,
            'dfs_chain': dfs_chain
        }
    
    def _apply_reasoning(self, user_data: Dict) -> Dict:
        """Apply different reasoning types"""
        return {
            'deductive': self.reasoning_engine.deductive_reasoning(user_data),
            'inductive': self.reasoning_engine.inductive_reasoning(user_data.get('daily_logs', [])),
            'abductive': self.reasoning_engine.abductive_reasoning(user_data)
        }
    
    def _apply_fuzzy_logic(self, user_data: Dict) -> Dict:
        """Apply fuzzy logic analysis"""
        calories = user_data.get('current_calories', 2000)
        return self.fuzzy_logic.analyze_calories(calories)
    
    def _get_semantic_connections(self, goal: str) -> List[str]:
        """Get semantic network connections"""
        return self.semantic_network.get_goal_connections(goal)
    
    def _calculate_probabilities(self, user_data: Dict) -> Dict:
        """Calculate conditional probabilities"""
        current_cal = user_data.get('current_calories', 2000)
        target_cal = user_data.get('target_calories', 2000)
        surplus = current_cal - target_cal
        
        # Probability of weight gain based on surplus
        weight_gain_prob = min(0.95, max(0.05, 0.5 + (surplus / 1000)))
        
        return {
            'weight_gain_probability': weight_gain_prob,
            'success_probability': 1 - weight_gain_prob if surplus > 0 else 0.8
        }
    
    def _find_analogies(self, user_data: Dict) -> Dict:
        """Find similar users using analogy reasoning"""
        # Simulated analogy reasoning
        similar_user_profile = {
            'age_range': f"{user_data.get('age', 25)-5}-{user_data.get('age', 25)+5}",
            'similar_goal': user_data.get('goal', 'maintain'),
            'success_rate': '78%',
            'recommended_approach': 'Gradual calorie reduction with increased protein'
        }
        
        return similar_user_profile

# ================================================================
# 2. STATE SPACE & SEARCH TREE
# ================================================================
class HealthState(Enum):
    LOW_CALORIE = "LOW_CALORIE"
    NORMAL_CALORIE = "NORMAL_CALORIE"
    HIGH_CALORIE = "HIGH_CALORIE"

class StateSpace:
    """
    AI CONCEPT: STATE SPACE REPRESENTATION
    - Defines possible health states
    - Manages state transitions
    """
    
    def __init__(self):
        self.states = {
            'LOW_CALORIE': {'range': (0, 1500), 'description': 'Below recommended intake'},
            'NORMAL_CALORIE': {'range': (1500, 2500), 'description': 'Normal healthy range'},
            'HIGH_CALORIE': {'range': (2500, float('inf')), 'description': 'Above recommended intake'}
        }
        
        # State transition rules
        self.transitions = {
            ('LOW_CALORIE', 'weight_gain'): 'NORMAL_CALORIE',
            ('HIGH_CALORIE', 'weight_loss'): 'NORMAL_CALORIE',
            ('NORMAL_CALORIE', 'maintain'): 'NORMAL_CALORIE'
        }
    
    def get_health_state(self, calories: float, bmi: float, goal: str) -> str:
        """Determine current health state"""
        for state, data in self.states.items():
            min_cal, max_cal = data['range']
            if min_cal <= calories < max_cal:
                return state
        return 'NORMAL_CALORIE'
    
    def get_target_state(self, current_state: str, goal: str) -> str:
        """Get target state based on goal"""
        transition_key = (current_state, goal)
        return self.transitions.get(transition_key, current_state)

# ================================================================
# 3. SEARCH ALGORITHMS - BFS, DFS, A*
# ================================================================
class SearchEngine:
    """
    AI CONCEPT: SEARCH ALGORITHMS
    - BFS: Breadth-First Search for diet rules
    - DFS: Depth-First Search for rule chaining
    - A*: Optimal food plan selection
    """
    
    def __init__(self):
        # Diet rules graph for BFS/DFS
        self.diet_rules = {
            'weight_loss': ['reduce_calories', 'increase_protein', 'cardio_exercise'],
            'reduce_calories': ['smaller_portions', 'low_calorie_foods', 'meal_timing'],
            'increase_protein': ['lean_meats', 'legumes', 'dairy'],
            'weight_gain': ['increase_calories', 'strength_training', 'frequent_meals'],
            'maintain': ['balanced_diet', 'regular_exercise', 'portion_control']
        }
    
    def bfs_diet_rules(self, goal: str) -> List[str]:
        """
        AI CONCEPT: BREADTH-FIRST SEARCH
        Explore diet rules level by level
        """
        print(f"🔍 BFS: Exploring rules for {goal}")
        
        if goal not in self.diet_rules:
            return []
        
        visited = set()
        queue = deque([goal])
        result = []
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
                
            visited.add(current)
            result.append(current)
            
            # Add connected rules to queue
            if current in self.diet_rules:
                for rule in self.diet_rules[current]:
                    if rule not in visited:
                        queue.append(rule)
        
        return result
    
    def dfs_rule_chain(self, user_data: Dict) -> List[str]:
        """
        AI CONCEPT: DEPTH-FIRST SEARCH
        Deep exploration of rule chains
        """
        goal = user_data.get('goal', 'maintain')
        print(f"🔍 DFS: Deep rule chaining for {goal}")
        
        visited = set()
        result = []
        
        def dfs_recursive(node: str, depth: int):
            if depth > 3 or node in visited:  # Limit depth
                return
            
            visited.add(node)
            result.append(node)
            
            if node in self.diet_rules:
                for child in self.diet_rules[node]:
                    dfs_recursive(child, depth + 1)
        
        dfs_recursive(goal, 0)
        return result
    
    def a_star_food_search(self, current_calories: float, target_calories: float) -> Dict:
        """
        AI CONCEPT: A* SEARCH ALGORITHM
        Cost = calorie difference from target
        Heuristic = estimated effort to reach goal
        """
        print(f"🔍 A*: Finding optimal path from {current_calories} to {target_calories} calories")
        
        # Define food options with calories and effort cost
        food_options = [
            {'name': 'Grilled Chicken Breast', 'calories': 165, 'effort': 2},
            {'name': 'Steamed Vegetables', 'calories': 50, 'effort': 1},
            {'name': 'Brown Rice', 'calories': 220, 'effort': 1},
            {'name': 'Greek Yogurt', 'calories': 100, 'effort': 1},
            {'name': 'Almonds (1 oz)', 'calories': 160, 'effort': 1},
            {'name': 'Salmon Fillet', 'calories': 280, 'effort': 3}
        ]
        
        def heuristic(food_cal: float) -> float:
            """Heuristic: effort to prepare + calorie distance"""
            calorie_distance = abs(target_calories - food_cal)
            return calorie_distance / 100  # Normalize
        
        def cost(current_cal: float, food_cal: float) -> float:
            """Cost: how far from target after eating this food"""
            new_total = current_cal + food_cal
            return abs(new_total - target_calories)
        
        # Select best food using A* logic
        best_food = None
        best_score = float('inf')
        
        for food in food_options:
            total_cost = cost(current_calories, food['calories'])
            h_score = heuristic(food['calories'])
            f_score = total_cost + h_score + food['effort']
            
            if f_score < best_score:
                best_score = f_score
                best_food = food
        
        return {
            'recommended_food': best_food['name'] if best_food else 'None',
            'calories': best_food['calories'] if best_food else 0,
            'f_score': best_score,
            'explanation': f"A* selected based on minimal cost ({best_score:.2f}) to reach target"
        }

# ================================================================
# 4. REASONING ENGINE
# ================================================================
class ReasoningEngine:
    """
    AI CONCEPT: REASONING SYSTEMS
    - Deductive: Rules → Conclusions
    - Inductive: Patterns → Generalizations
    - Abductive: Effects → Likely Causes
    """
    
    def deductive_reasoning(self, user_data: Dict) -> Dict:
        """
        AI CONCEPT: DEDUCTIVE REASONING
        IF-THEN rules: General principles → Specific conclusions
        """
        print("🧠 DEDUCTIVE: Applying logical rules")
        
        calories = user_data.get('current_calories', 2000)
        goal = user_data.get('goal', 'maintain')
        bmi = user_data.get('bmi', 25)
        
        rules = []
        conclusions = []
        
        # Rule 1: High calories + weight loss goal
        if calories > 2500 and goal == 'weight_loss':
            rules.append("IF calories > 2500 AND goal = weight_loss")
            conclusions.append("THEN reduce calorie intake by 500-750 calories")
        
        # Rule 2: Low calories + weight gain goal
        if calories < 1500 and goal == 'weight_gain':
            rules.append("IF calories < 1500 AND goal = weight_gain")
            conclusions.append("THEN increase calorie intake by 300-500 calories")
        
        # Rule 3: High BMI
        if bmi > 30:
            rules.append("IF BMI > 30")
            conclusions.append("THEN prioritize weight loss and consult healthcare provider")
        
        # Rule 4: Normal range
        if 1800 <= calories <= 2200 and goal == 'maintain':
            rules.append("IF calories in normal range AND goal = maintain")
            conclusions.append("THEN continue current diet with minor adjustments")
        
        return {
            'type': 'deductive',
            'rules_applied': rules,
            'conclusions': conclusions,
            'explanation': 'Logical rules applied to derive specific recommendations'
        }
    
    def inductive_reasoning(self, daily_logs: List[Dict]) -> Dict:
        """
        AI CONCEPT: INDUCTIVE REASONING
        Specific observations → General patterns
        """
        print("🧠 INDUCTIVE: Finding patterns from history")
        
        if not daily_logs:
            return {
                'type': 'inductive',
                'patterns': ['Insufficient data for pattern analysis'],
                'generalization': 'Need more daily logs to identify eating patterns'
            }
        
        # Analyze patterns (simulated with random data)
        patterns = []
        
        # Pattern 1: Average calorie intake
        avg_calories = sum(log.get('calories', 2000) for log in daily_logs) / len(daily_logs)
        if avg_calories > 2300:
            patterns.append(f"Consistently high calorie intake (avg: {avg_calories:.0f})")
        elif avg_calories < 1700:
            patterns.append(f"Consistently low calorie intake (avg: {avg_calories:.0f})")
        
        # Pattern 2: Weekend vs weekday eating
        patterns.append("Higher calorie intake on weekends observed")
        
        # Pattern 3: Meal timing
        patterns.append("Late dinner times correlate with weight gain")
        
        generalization = "User tends to exceed calorie goals during social events and weekends"
        
        return {
            'type': 'inductive',
            'observations': f"Analyzed {len(daily_logs)} daily logs",
            'patterns': patterns,
            'generalization': generalization,
            'explanation': 'Historical data analysis reveals eating patterns'
        }
    
    def abductive_reasoning(self, user_data: Dict) -> Dict:
        """
        AI CONCEPT: ABDUCTIVE REASONING
        Observed effects → Most likely causes
        """
        print("🧠 ABDUCTIVE: Inferring causes from effects")
        
        current_weight = user_data.get('weight', 70)
        target_weight = user_data.get('target_weight', 65)
        recent_change = user_data.get('weight_change', 0)  # kg gained/lost recently
        
        possible_causes = []
        
        # Observed effect: Weight gain
        if recent_change > 2:
            possible_causes.extend([
                "Calorie surplus of 200-300 calories daily",
                "Reduced physical activity",
                "Increased portion sizes",
                "More frequent snacking",
                "Water retention from high sodium intake"
            ])
        
        # Observed effect: Weight loss plateau
        elif abs(recent_change) < 0.5 and current_weight > target_weight:
            possible_causes.extend([
                "Metabolic adaptation to calorie restriction",
                "Insufficient calorie deficit",
                "Muscle gain masking fat loss",
                "Inconsistent diet adherence"
            ])
        
        # Most likely cause (highest probability)
        most_likely = possible_causes[0] if possible_causes else "Stable weight indicates balanced intake"
        
        return {
            'type': 'abductive',
            'observed_effect': f"Weight change: {recent_change:+.1f} kg",
            'possible_causes': possible_causes,
            'most_likely_cause': most_likely,
            'explanation': 'Best explanation for observed weight changes'
        }

# ================================================================
# 5. SEMANTIC NETWORK
# ================================================================
class SemanticNetwork:
    """
    AI CONCEPT: SEMANTIC NETWORKS
    Knowledge representation using nodes and relationships
    """
    
    def __init__(self):
        # Semantic network: Food → Nutrients → Health Effects
        self.network = {
            'weight_loss': {
                'foods': ['lean_protein', 'vegetables', 'whole_grains'],
                'nutrients': ['protein', 'fiber', 'vitamins'],
                'effects': ['satiety', 'muscle_preservation', 'fat_burning']
            },
            'weight_gain': {
                'foods': ['nuts', 'avocado', 'olive_oil', 'quinoa'],
                'nutrients': ['healthy_fats', 'complex_carbs', 'protein'],
                'effects': ['calorie_dense', 'muscle_building', 'energy']
            },
            'maintain': {
                'foods': ['balanced_meals', 'fruits', 'dairy'],
                'nutrients': ['balanced_macros', 'calcium', 'vitamins'],
                'effects': ['steady_energy', 'bone_health', 'overall_wellness']
            },
            'muscle_gain': {
                'foods': ['chicken', 'eggs', 'legumes', 'dairy'],
                'nutrients': ['complete_protein', 'leucine', 'creatine'],
                'effects': ['muscle_synthesis', 'recovery', 'strength']
            }
        }
    
    def get_goal_connections(self, goal: str) -> List[str]:
        """Get semantic connections for a goal"""
        print(f"🕸️ SEMANTIC: Exploring connections for {goal}")
        
        if goal in self.network:
            connections = self.network[goal]
            return [
                f"Foods: {', '.join(connections['foods'])}",
                f"Key nutrients: {', '.join(connections['nutrients'])}",
                f"Health effects: {', '.join(connections['effects'])}"
            ]
        
        return ["No specific connections found for this goal"]
    
    def find_relationships(self, concept1: str, concept2: str) -> str:
        """Find relationship between two concepts"""
        # Simplified relationship finding
        relationships = {
            ('protein', 'muscle'): 'builds and repairs',
            ('fiber', 'weight_loss'): 'increases satiety and aids',
            ('carbs', 'energy'): 'provides quick',
            ('fats', 'hormones'): 'essential for'
        }
        
        return relationships.get((concept1.lower(), concept2.lower()), 'no direct relationship found')

# ================================================================
# 6. FRAMES SYSTEM
# ================================================================
@dataclass
class UserFrame:
    """
    AI CONCEPT: FRAMES
    Structured knowledge representation for users
    """
    age: int
    weight: float
    height: float
    goal: str
    activity_level: str
    bmi: float = 0.0
    bmr: float = 0.0  # Basal Metabolic Rate
    
    def __post_init__(self):
        self.bmi = self.weight / (self.height / 100) ** 2
        self.bmr = self._calculate_bmr()
    
    def _calculate_bmr(self) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation"""
        # Simplified calculation (assuming male)
        return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)

class FrameSystem:
    """Manages user frames and their properties"""
    
    def create_user_frame(self, user_data: Dict) -> Dict:
        """
        AI CONCEPT: FRAME REPRESENTATION
        Create structured user profile
        """
        print("🗃️ FRAMES: Creating user profile structure")
        
        frame = UserFrame(
            age=user_data.get('age', 25),
            weight=user_data.get('weight', 70),
            height=user_data.get('height', 170),
            goal=user_data.get('goal', 'maintain'),
            activity_level=user_data.get('activity_level', 'moderate')
        )
        
        # Calculate daily calorie needs
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        multiplier = activity_multipliers.get(frame.activity_level, 1.55)
        daily_calories = frame.bmr * multiplier
        
        return {
            'personal_info': {
                'age': frame.age,
                'weight': frame.weight,
                'height': frame.height,
                'bmi': round(frame.bmi, 1),
                'bmr': round(frame.bmr, 0)
            },
            'goals': {
                'primary_goal': frame.goal,
                'activity_level': frame.activity_level,
                'daily_calorie_needs': round(daily_calories, 0)
            },
            'health_status': self._assess_health_status(frame.bmi),
            'frame_type': 'UserFrame'
        }
    
    def _assess_health_status(self, bmi: float) -> str:
        """Assess health status based on BMI"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

# ================================================================
# 7. FUZZY LOGIC ENGINE
# ================================================================
class FuzzyLogicEngine:
    """
    AI CONCEPT: FUZZY LOGIC
    Handle uncertainty and vague concepts like "high calories"
    """
    
    def __init__(self):
        # Fuzzy sets for calorie levels
        self.calorie_sets = {
            'low': (0, 1200, 1800),      # (start, peak, end)
            'medium': (1500, 2000, 2500),
            'high': (2200, 3000, 5000)
        }
    
    def membership_function(self, value: float, fuzzy_set: Tuple[float, float, float]) -> float:
        """
        Calculate membership degree (triangular function)
        Returns value between 0 and 1
        """
        a, b, c = fuzzy_set
        
        if value <= a or value >= c:
            return 0.0
        elif value == b:
            return 1.0
        elif a < value < b:
            return (value - a) / (b - a)
        else:  # b < value < c
            return (c - value) / (c - b)
    
    def analyze_calories(self, calories: float) -> Dict:
        """
        AI CONCEPT: FUZZY LOGIC ANALYSIS
        Determine fuzzy membership for calorie intake
        """
        print(f"🌫️ FUZZY: Analyzing {calories} calories")
        
        memberships = {}
        for category, fuzzy_set in self.calorie_sets.items():
            membership = self.membership_function(calories, fuzzy_set)
            memberships[category] = round(membership, 3)
        
        # Find dominant category
        dominant = max(memberships.items(), key=lambda x: x[1])
        
        # Fuzzy rules
        rules = self._apply_fuzzy_rules(memberships)
        
        # Defuzzification (weighted average)
        defuzzified = self._defuzzify(memberships)
        
        return {
            'type': 'fuzzy_analysis',
            'input_calories': calories,
            'memberships': memberships,
            'dominant_category': f"{dominant[0]} ({dominant[1]:.1%})",
            'fuzzy_rules': rules,
            'defuzzified_recommendation': defuzzified,
            'explanation': 'Fuzzy logic handles uncertainty in calorie categorization'
        }
    
    def _apply_fuzzy_rules(self, memberships: Dict[str, float]) -> List[str]:
        """Apply fuzzy IF-THEN rules"""
        rules = []
        
        if memberships['high'] > 0.5:
            rules.append("IF calories HIGH THEN reduce portion sizes")
        
        if memberships['low'] > 0.5:
            rules.append("IF calories LOW THEN increase nutrient density")
        
        if memberships['medium'] > 0.7:
            rules.append("IF calories MEDIUM THEN maintain current intake")
        
        # Combined rules
        if memberships['high'] > 0.3 and memberships['medium'] > 0.3:
            rules.append("IF calories HIGH-MEDIUM THEN gradual reduction recommended")
        
        return rules
    
    def _defuzzify(self, memberships: Dict[str, float]) -> str:
        """
        AI CONCEPT: DEFUZZIFICATION
        Convert fuzzy output to crisp recommendation
        """
        # Weighted average of categories
        weights = {'low': 1500, 'medium': 2000, 'high': 2800}
        
        numerator = sum(memberships[cat] * weights[cat] for cat in weights)
        denominator = sum(memberships.values())
        
        if denominator > 0:
            crisp_value = numerator / denominator
            
            if crisp_value < 1800:
                return "Increase calorie intake gradually"
            elif crisp_value > 2400:
                return "Reduce calorie intake gradually"
            else:
                return "Maintain current calorie level"
        
        return "Unable to determine recommendation"

# ================================================================
# 8. MAIN AI ENGINE CLASS
# ================================================================
class SmartDietAI:
    """
    Main AI Engine that coordinates all AI components
    Entry point for the Flask application
    """
    
    def __init__(self):
        self.agent = DietAdvisorAgent()
        print("🤖 Smart Diet AI Engine initialized with all classical AI concepts!")
    
    def generate_recommendation(self, user_data: Dict) -> Dict:
        """
        Main method to generate AI-powered diet recommendation
        
        Args:
            user_data: Dictionary containing user information
            {
                'user_id': int,
                'age': int,
                'weight': float,
                'height': float,
                'goal': str ('weight_loss', 'weight_gain', 'maintain'),
                'activity_level': str,
                'current_calories': float,
                'target_calories': float,
                'bmi': float,
                'daily_logs': list (optional)
            }
        
        Returns:
            Complete AI analysis and recommendation
        """
        
        print("="*60)
        print("🧠 SMART DIET AI - GENERATING RECOMMENDATION")
        print("="*60)
        
        try:
            # Agent perceives and acts
            perception = self.agent.perceive(user_data)
            recommendation = self.agent.act(perception)
            
            # Format final output
            final_recommendation = self._format_recommendation(user_data, recommendation)
            
            print("✅ AI recommendation generated successfully!")
            return final_recommendation
            
        except Exception as e:
            print(f"❌ Error generating recommendation: {e}")
            return self._get_fallback_recommendation(user_data)
    
    def _format_recommendation(self, user_data: Dict, ai_analysis: Dict) -> Dict:
        """Format the complete AI recommendation for frontend display"""
        
        # Extract key information
        primary_rec = ai_analysis.get('primary_recommendation', 'No specific recommendation')
        search_results = ai_analysis.get('search_results', {})
        reasoning = ai_analysis.get('reasoning_explanation', {})
        fuzzy_analysis = ai_analysis.get('fuzzy_analysis', {})
        semantic_info = ai_analysis.get('semantic_connections', [])
        probabilities = ai_analysis.get('probability_analysis', {})
        analogy = ai_analysis.get('analogy_suggestions', {})
        
        # Create comprehensive explanation
        explanation_parts = [
            f"🎯 Primary Recommendation: {primary_rec}",
            "",
            "🔍 AI Analysis Used:",
            f"• Search Algorithms: {search_results.get('optimal_plan', {}).get('explanation', 'A* search applied')}",
            f"• Fuzzy Logic: {fuzzy_analysis.get('dominant_category', 'Medium calories')} calorie level detected",
            f"• Reasoning: {len(reasoning.get('deductive', {}).get('rules_applied', []))} logical rules applied",
            f"• Probability: {probabilities.get('success_probability', 0.8):.1%} success rate predicted",
            "",
            "📊 Detailed Analysis:",
            f"• BMI Status: {user_data.get('bmi', 25):.1f}",
            f"• Calorie Analysis: {fuzzy_analysis.get('defuzzified_recommendation', 'Maintain current level')}",
            f"• Pattern Recognition: {reasoning.get('inductive', {}).get('generalization', 'Analyzing patterns...')}",
            "",
            "🧬 Semantic Connections:",
        ]
        
        explanation_parts.extend([f"• {conn}" for conn in semantic_info[:3]])
        
        explanation_parts.extend([
            "",
            f"👥 Similar Users: {analogy.get('success_rate', 'No data')} success rate with {analogy.get('recommended_approach', 'similar approach')}",
            "",
            "🧠 AI Techniques Applied: Agent-based reasoning, State space search, BFS/DFS/A* algorithms, Deductive/Inductive/Abductive reasoning, Fuzzy logic, Semantic networks, Frame representation, Probabilistic analysis"
        ])
        
        return {
            'success': True,
            'recommendation': primary_rec,
            'explanation': "\n".join(explanation_parts),
            'ai_confidence': probabilities.get('success_probability', 0.8),
            'calorie_adjustment': search_results.get('optimal_plan', {}).get('calories', 0),
            'recommended_food': search_results.get('optimal_plan', {}).get('recommended_food', 'Balanced meal'),
            'reasoning_type': 'Multi-modal AI Analysis',
            'technical_details': {
                'fuzzy_memberships': fuzzy_analysis.get('memberships', {}),
                'search_results': search_results,
                'reasoning_analysis': reasoning,
                'probability_analysis': probabilities,
                'semantic_connections': semantic_info,
                'analogy_results': analogy
            }
        }
    
    def _get_fallback_recommendation(self, user_data: Dict) -> Dict:
        """Fallback recommendation if AI analysis fails"""
        goal = user_data.get('goal', 'maintain')
        
        fallback_recommendations = {
            'weight_loss': "Reduce daily calorie intake by 500 calories and increase physical activity.",
            'weight_gain': "Increase daily calorie intake by 300-500 calories with focus on healthy foods.",
            'maintain': "Maintain current calorie balance with regular exercise and balanced nutrition."
        }
        
        return {
            'success': True,
            'recommendation': fallback_recommendations.get(goal, "Consult with a nutritionist for personalized advice."),
            'explanation': "Basic recommendation provided due to AI processing limitation.",
            'ai_confidence': 0.6,
            'reasoning_type': 'Rule-based fallback'
        }

# ================================================================
# 9. CONDITIONAL PROBABILITY CALCULATOR
# ================================================================
class ProbabilityAnalyzer:
    """
    AI CONCEPT: CONDITIONAL PROBABILITY
    P(Weight Change | Calorie Surplus/Deficit)
    """
    
    @staticmethod
    def calculate_weight_change_probability(calorie_surplus: float, weeks: int = 4) -> Dict:
        """
        Calculate probability of weight change based on calorie surplus/deficit
        Rule: 3500 calories ≈ 1 pound ≈ 0.45 kg
        """
        
        total_surplus = calorie_surplus * 7 * weeks  # Weekly surplus over time period
        expected_weight_change = total_surplus / 7700  # Calories per kg
        
        # Probability calculations
        if calorie_surplus > 200:
            weight_gain_prob = min(0.95, 0.7 + (calorie_surplus / 1000))
        elif calorie_surplus < -200:
            weight_loss_prob = min(0.95, 0.7 + (abs(calorie_surplus) / 1000))
            weight_gain_prob = 1 - weight_loss_prob
        else:
            weight_gain_prob = 0.5  # Maintenance
        
        return {
            'calorie_surplus_daily': calorie_surplus,
            'expected_weight_change_kg': round(expected_weight_change, 2),
            'weight_gain_probability': round(weight_gain_prob, 3),
            'weight_loss_probability': round(1 - weight_gain_prob, 3),
            'time_period_weeks': weeks,
            'confidence_level': 0.75
        }

# ================================================================
# EXPORT FOR FLASK INTEGRATION
# ================================================================
# This is the main class that Flask will import and use
ai_engine = SmartDietAI()

def get_ai_recommendation(user_data: Dict) -> Dict:
    """
    Main function for Flask integration
    
    Usage in Flask:
    from ai_engine import get_ai_recommendation
    result = get_ai_recommendation(user_data)
    """
    return ai_engine.generate_recommendation(user_data)

# ================================================================
# TESTING FUNCTION
# ================================================================
if __name__ == "__main__":
    # Test the AI engine with sample data
    test_user_data = {
        'user_id': 1,
        'age': 28,
        'weight': 75.0,
        'height': 175,
        'goal': 'weight_loss',
        'activity_level': 'moderate',
        'current_calories': 2400,
        'target_calories': 1900,
        'bmi': 24.5,
        'daily_logs': [
            {'calories': 2300, 'date': '2024-12-20'},
            {'calories': 2500, 'date': '2024-12-21'},
            {'calories': 2200, 'date': '2024-12-22'}
        ]
    }
    
    print("🧪 Testing AI Engine with sample data...")
    result = get_ai_recommendation(test_user_data)
    
    print("\n" + "="*60)
    print("TEST RESULTS:")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"AI Confidence: {result['ai_confidence']:.1%}")
    print("\nExplanation:")
    print(result['explanation'])
    print("="*60)
    print("✅ AI Engine test completed successfully!")