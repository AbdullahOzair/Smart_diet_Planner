================================================================================
            SMART DIET PLANNER - AI MODULE VIVA GUIDE
           (For Lab Viva & Demonstration - December 2024)
================================================================================

This document explains the AI concepts implemented in our Smart Diet Planner
and maps them to the lab syllabus topics.

================================================================================
                        TABLE OF CONTENTS
================================================================================
1. Overview of AI Module
2. AI Concepts Demonstrated
   2.1 AI Agent (Lab 2-3)
   2.2 State Space Search & BFS (Lab 4-5)
   2.3 A* Search Algorithm (Lab 7)
   2.4 Deductive Reasoning (Lab 8)
   2.5 Fuzzy Logic (Lab 10)
   2.6 Conditional Probability (Lab 11)
3. Code Structure
4. Frontend-Backend Mapping
5. How to Demonstrate
6. Sample Questions & Answers

================================================================================
                    1. OVERVIEW OF AI MODULE
================================================================================

Location: flask_app/ai_module/viva_ai_engine.py

The AI module is responsible for generating personalized diet recommendations
by analyzing user data and applying multiple AI techniques.

Main Entry Point:
    get_ai_recommendation(user_id, goal)
    
    - Called from: flask_app/app.py → /ai-recommendation route
    - Returns: Dictionary with recommendation, explanation, foods, activities, 
               fuzzy evaluation, risk assessment

================================================================================
                    2. AI CONCEPTS DEMONSTRATED
================================================================================

------------------------------------------------------------------------------
2.1 AI AGENT (Lab 2-3)
------------------------------------------------------------------------------
DEFINITION:
    An AI agent is an entity that:
    - PERCEIVES its environment through sensors
    - THINKS/DECIDES based on perceived information
    - ACTS on the environment through actuators

OUR IMPLEMENTATION:
    Class: DietPlannerAgent (line 110)
    
    Methods:
    - perceive(): Collects user data from database (daily logs, meals, activities)
    - decide(): Applies AI techniques (reasoning, fuzzy logic, search, probability)
    - act(): Returns the final recommendation

CODE LOCATION:
    viva_ai_engine.py, lines 110-280

FRONTEND CONNECTION:
    - User opens "AI Recommendations" page
    - Clicks "Get AI Recommendation"
    - Agent perceives their data, decides, and acts
    - Result shown in green header card

VIVA QUESTION:
    Q: What is an AI agent?
    A: An AI agent is an entity that perceives its environment, makes decisions
       based on that information, and takes actions. In our system, the 
       DietPlannerAgent perceives user health data, decides using AI techniques
       like reasoning and fuzzy logic, and acts by providing diet recommendations.

------------------------------------------------------------------------------
2.2 STATE SPACE SEARCH & BFS (Lab 4-5)
------------------------------------------------------------------------------
DEFINITION:
    - State Space: All possible states/configurations of a problem
    - BFS (Breadth-First Search): Explores level by level using a queue (FIFO)
    
    Search Tree for our system:
    
                    [All Foods]
                   /    |    \
           [Proteins] [Carbs] [Healthy Fats]
           /    \       |       \
      [Chicken][Fish] [Rice]   [Nuts]

OUR IMPLEMENTATION:
    Class: FoodSearchEngine (line 300)
    Method: bfs_search_categories()
    
    Algorithm:
    1. Start with "All Foods" (root state)
    2. Use a queue (FIFO)
    3. Pop from front, add children to back
    4. Explore all food categories level by level

CODE LOCATION:
    viva_ai_engine.py, lines 310-365

FRONTEND CONNECTION:
    - Food recommendations card shows "A* Search: Optimal Foods"
    - BFS first explores all categories to identify relevant food groups

VIVA QUESTION:
    Q: Explain BFS in the context of your project.
    A: BFS explores the food category tree level by level. Starting from 
       "All Foods", it first explores Proteins, Carbs, Healthy Fats (level 1),
       then Chicken, Fish, Rice, Nuts (level 2). This ensures we consider all
       food categories before diving deep into specific foods.

------------------------------------------------------------------------------
2.3 A* SEARCH ALGORITHM (Lab 7)
------------------------------------------------------------------------------
DEFINITION:
    A* is a best-first search algorithm that uses:
    f(n) = g(n) + h(n)
    
    Where:
    - g(n) = Cost from start to current node
    - h(n) = Heuristic estimate to goal
    - f(n) = Total estimated cost

OUR IMPLEMENTATION:
    Class: FoodSearchEngine (line 300)
    Method: a_star_rank_foods() (line 370)
    
    In our system:
    - g(n) = Calorie cost (normalized: 500 cal = 1.0)
    - h(n) = Nutrition heuristic (inverted: good nutrition = low h(n))
    - f(n) = Combined score (lower is better)
    
    For weight loss: Low calories + High nutrition = Best choice
    For weight gain: High calories + High nutrition = Best choice

CODE LOCATION:
    viva_ai_engine.py, lines 370-430

FRONTEND CONNECTION:
    - Orange card: "A* Search: Optimal Foods"
    - Shows foods ranked by f(n) score
    - Displays: food name, calories, protein, f(n) value

VIVA QUESTION:
    Q: How does A* work in your diet recommendation?
    A: A* ranks foods by combining calorie cost (g(n)) and nutrition benefit 
       (h(n)). For weight loss, it prioritizes low-calorie, high-nutrition foods.
       The food with the lowest f(n) value is the "optimal" choice. For example,
       if Beef Jerky has f(n)=0.85 and Pizza has f(n)=1.5, A* recommends the jerky.

------------------------------------------------------------------------------
2.4 DEDUCTIVE REASONING (Lab 8)
------------------------------------------------------------------------------
DEFINITION:
    Deductive reasoning applies general rules to specific situations to derive
    conclusions. It follows: Premises → Conclusion (guaranteed true if premises true)

OUR IMPLEMENTATION:
    Class: DeductiveReasoner (line 450)
    
    Knowledge Base (Rules):
    - R1: IF goal="lose" AND calories="high" THEN reduce_calories
    - R2: IF goal="lose" AND protein="low" THEN increase_protein
    - R3: IF goal="gain" AND calories="low" THEN increase_calories
    - R4: IF goal="gain" AND protein="low" THEN increase_protein
    - R5: IF activity="low" THEN increase_activity
    - R6: IF mood="low" AND sleep="low" THEN improve_sleep
    - R7: IF goal="maintain" AND calories="balanced" THEN maintain_current

CODE LOCATION:
    viva_ai_engine.py, lines 450-580

FRONTEND CONNECTION:
    - Black card: "AI Reasoning Process"
    - Shows: "📜 DEDUCTIVE REASONING:"
    - Lists which rules fired and their explanations

VIVA QUESTION:
    Q: Explain deductive reasoning in your project.
    A: We have a knowledge base of IF-THEN rules. When a user wants to lose 
       weight and their calorie intake is high, Rule R1 fires: "IF goal=lose 
       AND calories=high THEN reduce_calories". The conclusion is guaranteed 
       because the premises (user goal and calorie status) are known facts.

------------------------------------------------------------------------------
2.5 FUZZY LOGIC (Lab 10)
------------------------------------------------------------------------------
DEFINITION:
    Unlike binary logic (TRUE/FALSE), fuzzy logic deals with degrees of truth.
    A value can be "partially true" with membership between 0 and 1.
    
    Membership Function (Triangular):
    
                1 |       /\
                  |      /  \
                  |     /    \
                0 |____/______\____
                    a    b    c

OUR IMPLEMENTATION:
    Class: FuzzyEvaluator (line 600)
    
    Fuzzy Sets for Calories:
    - LOW: peaks at 1000 cal, range [0, 1500]
    - MEDIUM: peaks at 1800 cal, range [1200, 2200]
    - HIGH: peaks at 2500 cal, range [2000, 4000]
    
    Example: If user consumes 1900 calories:
    - Membership in LOW = 0%
    - Membership in MEDIUM = 60%
    - Membership in HIGH = 40%

CODE LOCATION:
    viva_ai_engine.py, lines 600-720

FRONTEND CONNECTION:
    - Purple card: "Fuzzy Logic Evaluation"
    - Shows: "Your calorie intake is 60% MEDIUM"
    - Shows: "Your activity level is 30% LOW"
    - Shows: "Your sleep quality is 100% ADEQUATE"

VIVA QUESTION:
    Q: What is fuzzy logic and how do you use it?
    A: Fuzzy logic allows values to belong to multiple categories with different
       degrees. A calorie intake of 1900 might be 60% MEDIUM and 40% HIGH.
       We use triangular membership functions to calculate these degrees.
       This is more realistic than saying "1900 is exactly MEDIUM".

------------------------------------------------------------------------------
2.6 CONDITIONAL PROBABILITY (Lab 11)
------------------------------------------------------------------------------
DEFINITION:
    P(A|B) = Probability of A given that B has occurred
    
    Bayes' Theorem: P(A|B) = P(B|A) × P(A) / P(B)

OUR IMPLEMENTATION:
    Class: ProbabilityCalculator (line 750)
    
    We calculate: P(outcome | user's conditions)
    
    Base Probabilities:
    - P(weight_gain) = 30%
    - P(weight_loss) = 30%
    - P(health_risk) = 20%
    - P(energy_drop) = 25%
    
    Conditional Multipliers:
    - If high_calories: P(weight_gain) × 1.5
    - If low_activity: P(weight_gain) × 1.3
    - If poor_sleep: P(health_risk) × 1.3
    
    Example:
    User has high calories + low activity:
    P(weight_gain) = 30% × 1.5 × 1.3 = 58.5%

CODE LOCATION:
    viva_ai_engine.py, lines 750-850

FRONTEND CONNECTION:
    - Red card: "Conditional Probability"
    - Shows: "P(outcome | your conditions)"
    - Displays risk percentages: "Weight Gain: 58%"
    - Shows warning if any risk > 40%

VIVA QUESTION:
    Q: How do you use conditional probability?
    A: We calculate the probability of outcomes like weight gain given the 
       user's conditions. If a user has high calorie intake and low activity,
       we multiply the base probability by condition-specific multipliers:
       P(weight_gain | high_cal, low_activity) = 0.30 × 1.5 × 1.3 = 0.585 (58.5%)

================================================================================
                    3. CODE STRUCTURE
================================================================================

flask_app/ai_module/viva_ai_engine.py
├── DOCUMENTATION (lines 1-60)
│   └── Explains all 6 AI concepts
│
├── DATABASE CONNECTION (lines 65-100)
│   └── get_connection(), execute_query()
│
├── AI AGENT (lines 110-280)
│   └── DietPlannerAgent class
│       ├── perceive() - Get user data
│       ├── decide() - Apply AI techniques
│       └── act() - Return recommendation
│
├── STATE SPACE SEARCH (lines 300-440)
│   └── FoodSearchEngine class
│       ├── bfs_search_categories()
│       └── a_star_rank_foods()
│
├── DEDUCTIVE REASONING (lines 450-580)
│   └── DeductiveReasoner class
│       ├── rules[] - Knowledge base
│       ├── evaluate_status()
│       └── apply_rules()
│
├── FUZZY LOGIC (lines 600-720)
│   └── FuzzyEvaluator class
│       ├── calorie_sets, activity_sets, sleep_sets
│       ├── triangular_membership()
│       └── get_fuzzy_assessment()
│
├── CONDITIONAL PROBABILITY (lines 750-850)
│   └── ProbabilityCalculator class
│       ├── base_probabilities
│       ├── multipliers
│       └── calculate_conditional_probability()
│
└── MAIN FUNCTION (lines 1050-1100)
    └── get_ai_recommendation(user_id, goal)

================================================================================
                    4. FRONTEND-BACKEND MAPPING
================================================================================

User Action              → Backend Function          → What User Sees
--------------------------------------------------------------------------------
Click "AI Recommendation"→ ai_recommendation()      → Form with goal selection
Submit goal              → get_ai_recommendation()  → AI Analysis page
                         → DietPlannerAgent.perceive→ (Internal: fetch data)
                         → DietPlannerAgent.decide  → (Internal: apply AI)
                         → DietPlannerAgent.act     → Results displayed:

Results Display:
┌─────────────────────────────────────────────────────────────────────────┐
│ GREEN CARD: "AI Analysis Complete!" + Confidence %                      │
│ → Shows: Main recommendation text                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ BLACK CARD: "AI Reasoning Process"                                       │
│ → Shows: DEDUCTIVE REASONING rules that fired                           │
│ → Shows: FUZZY LOGIC evaluation summary                                 │
│ → Shows: RISK ASSESSMENT summary                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ ORANGE CARD: "A* Search: Optimal Foods"                                  │
│ → Shows: Foods ranked by f(n) = g(n) + h(n)                             │
│ → Shows: Name, Calories, Protein, f(n) score                            │
├─────────────────────────────────────────────────────────────────────────┤
│ BLUE CARD: "Recommended Activities"                                      │
│ → Shows: Activities with duration and calorie burn                      │
├─────────────────────────────────────────────────────────────────────────┤
│ PURPLE SIDEBAR: "Fuzzy Logic Evaluation"                                 │
│ → Shows: Membership degrees for calories, activity, sleep               │
├─────────────────────────────────────────────────────────────────────────┤
│ RED SIDEBAR: "Conditional Probability"                                   │
│ → Shows: P(outcome | conditions) for each risk                          │
├─────────────────────────────────────────────────────────────────────────┤
│ BLUE SIDEBAR: "AI Confidence"                                            │
│ → Shows: Confidence score based on data availability                    │
└─────────────────────────────────────────────────────────────────────────┘

================================================================================
                    5. HOW TO DEMONSTRATE
================================================================================

STEP 1: Start the Application
    cd flask_app
    python app.py
    Open: http://127.0.0.1:4001

STEP 2: Login
    Username: testuser
    Password: test123

STEP 3: Navigate to AI Recommendations
    Click "AI Recommendations" in sidebar
    OR click "Get Recommendation" on Goals page

STEP 4: Generate Recommendation
    Select a goal: "Lose Weight", "Gain Weight", or "Maintain Weight"
    Click "Get AI Recommendation"

STEP 5: Explain Each Section
    Point to each card and explain the AI concept:
    
    1. "This green header shows the AGENT's final action/recommendation"
    
    2. "This explanation section shows DEDUCTIVE REASONING - 
        see how rules R2 and R5 fired based on my data"
    
    3. "This orange card shows A* SEARCH results - foods ranked by f(n).
        The algorithm finds optimal foods by minimizing calorie cost 
        while maximizing nutrition benefit"
    
    4. "This purple card shows FUZZY LOGIC - my calorie intake is 60% MEDIUM.
        Unlike binary logic, values can partially belong to multiple sets"
    
    5. "This red card shows CONDITIONAL PROBABILITY - 
        P(weight_gain | high_cal, low_activity) = 58%.
        We apply Bayesian reasoning to assess health risks"

STEP 6: Show Code
    Open: flask_app/ai_module/viva_ai_engine.py
    Show relevant class for each concept

================================================================================
                    6. SAMPLE QUESTIONS & ANSWERS
================================================================================

Q1: What AI techniques have you used in your project?
A1: We have implemented 6 AI techniques:
    1. AI Agent - Perceive-Decide-Act cycle
    2. BFS - Breadth-first search of food categories
    3. A* Search - Optimal food selection using f(n)=g(n)+h(n)
    4. Deductive Reasoning - IF-THEN rules for diet advice
    5. Fuzzy Logic - Degree-based evaluation of metrics
    6. Conditional Probability - Risk assessment

Q2: Explain the role of the AI agent.
A2: The DietPlannerAgent class:
    - PERCEIVES: Fetches user's daily logs, meals, activities, mood from database
    - DECIDES: Applies deductive reasoning, fuzzy logic, probability, and search
    - ACTS: Returns a comprehensive diet recommendation

Q3: What is the difference between BFS and A*?
A3: BFS explores all nodes at current level before going deeper. It's uninformed.
    A* uses a heuristic f(n)=g(n)+h(n) to prioritize promising nodes. It's informed.
    In our system, BFS explores food categories, A* ranks specific foods by optimality.

Q4: How does fuzzy logic work?
A4: Traditional logic: Is calorie intake HIGH? Yes/No
    Fuzzy logic: How HIGH is the calorie intake? 40% HIGH, 60% MEDIUM
    We use triangular membership functions with (a, peak, c) parameters.

Q5: Explain conditional probability in your risk assessment.
A5: We calculate P(weight_gain | conditions).
    If user has high calories and low activity:
    P(weight_gain) = base(0.30) × high_cal(1.5) × low_activity(1.3) = 58.5%

Q6: Where is the knowledge base for deductive reasoning?
A6: In DeductiveReasoner.rules[] array. Each rule has:
    - conditions: {goal: 'lose', calorie_status: 'high'}
    - conclusion: 'reduce_calories'
    - explanation: "Reduce calories for weight loss"

================================================================================
                        GOOD LUCK WITH YOUR VIVA!
================================================================================
