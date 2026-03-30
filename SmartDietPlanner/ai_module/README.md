# AI Module - Smart Diet Planner

## Overview
This module contains all Classical AI implementations for the Smart Diet Planner application.

## Structure
```
ai_module/
├── __init__.py       # Package initializer
└── ai_engine.py      # Main AI engine (920 lines)
```

## AI Concepts Implemented

### 1. Intelligent Agent
- **Class:** `DietAdvisorAgent`
- **Purpose:** Autonomous agent that perceives user data and provides recommendations
- **Methods:** `perceive()`, `think()`, `act()`

### 2. State Space Representation
- **Class:** `StateSpace`
- **Purpose:** Represents health states and goal states
- **States:** Underweight, Normal, Overweight, Obese

### 3. Search Algorithms
- **Class:** `SearchEngine`
- **Algorithms:** BFS, DFS, A*
- **Purpose:** Find optimal diet plans

### 4. Reasoning Engine
- **Class:** `ReasoningEngine`
- **Types:** Forward Chaining, Backward Chaining, Abductive Reasoning
- **Purpose:** Logical inference and decision making

### 5. Fuzzy Logic
- **Class:** `FuzzyLogicEngine`
- **Purpose:** Handle imprecise data (calorie levels)
- **Categories:** Very Low, Low, Moderate, High, Very High

### 6. Semantic Networks
- **Class:** `SemanticNetwork`
- **Purpose:** Knowledge representation using graphs
- **Relationships:** is-a, requires, affects

### 7. Frame Systems
- **Class:** `FrameSystem`
- **Purpose:** Structured data representation
- **Frames:** User profiles with slots

### 8. STRIPS Planning
- **Class:** `STRIPSPlanner`
- **Purpose:** Goal-based action planning
- **Components:** Preconditions, Actions, Effects

### 9. Expert System
- **Class:** `ExpertSystem`
- **Purpose:** Rule-based decision making
- **Rules:** IF-THEN rules for diet advice

### 10. Production System
- **Class:** `ProductionSystem`
- **Purpose:** Pattern matching and rule execution
- **Features:** Conflict resolution

### 11. Probabilistic Reasoning
- **Class:** `BayesianReasoner`
- **Purpose:** Bayesian probability calculations
- **Use:** Predict health outcomes

### 12. Knowledge Representation
- **Multiple Formats:** Rules, Frames, Semantic Networks
- **Purpose:** Store and retrieve domain knowledge

## Usage

### Basic Usage
```python
from ai_module.ai_engine import get_ai_recommendation

user_data = {
    'current_calories': 2200,
    'bmi': 25.5,
    'goal': 'lose_weight',
    'activity_level': 'moderate'
}

recommendation = get_ai_recommendation(user_data)
print(recommendation)
```

### Advanced Usage
```python
from ai_module.ai_engine import DietAdvisorAgent

agent = DietAdvisorAgent()

# Perceive user data
perception = agent.perceive(user_data)

# Think and plan
plan = agent.think(perception)

# Execute and generate recommendation
recommendation = agent.act(plan)
```

## Integration with Flask

In `flask_app/app.py`:
```python
from ai_module.ai_engine import get_ai_recommendation

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    user_data = {
        'current_calories': session.get('current_calories'),
        'bmi': session.get('bmi'),
        'goal': session.get('goal'),
        'activity_level': session.get('activity_level')
    }
    
    recommendation = get_ai_recommendation(user_data)
    return jsonify({'recommendation': recommendation})
```

## File Organization

### Before (Unorganized)
```
SmartDietPlanner/
├── ai_engine.py          # AI file in root (confusing)
├── flask_app/
└── database/
```

### After (Organized)
```
SmartDietPlanner/
├── ai_module/            # Clear AI folder
│   ├── __init__.py
│   └── ai_engine.py
├── flask_app/
└── database/
```

## Benefits of Organization

1. **Clear Structure** - Easy to find AI-related code
2. **Modularity** - AI module is independent
3. **Maintainability** - Easy to update and extend
4. **Professional** - Industry-standard project structure

## Development

### Adding New AI Concepts
1. Edit `ai_module/ai_engine.py`
2. Add new class or function
3. Update `__init__.py` to export new functionality
4. Update this README

### Testing
```python
# Test individual AI components
from ai_module.ai_engine import FuzzyLogicEngine

fuzzy = FuzzyLogicEngine()
calorie_level = fuzzy.classify_calories(2500)
print(f"Calorie level: {calorie_level}")
```

## References

- AI Concepts based on Russell & Norvig's "Artificial Intelligence: A Modern Approach"
- Fuzzy Logic implementation inspired by Zadeh's fuzzy set theory
- Search algorithms from classic CS algorithms

---

**Part of Smart Diet Planner Project**
