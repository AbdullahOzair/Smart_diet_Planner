# Smart Diet Planner - Visual Architecture

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                    Web Browser (Client)                          │
│                   http://localhost:3001                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      FLASK APPLICATION                           │
│                      (flask_app/app.py)                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    ROUTES                                 │  │
│  │  /                  - Home/Login page                     │  │
│  │  /login            - User authentication                  │  │
│  │  /register         - New user registration                │  │
│  │  /user_dashboard   - User main dashboard                  │  │
│  │  /admin_dashboard  - Admin control panel                  │  │
│  │  /log_meal         - Log meal entries                     │  │
│  │  /log_activity     - Log activity entries                 │  │
│  │  /get_recommendation - AI-based recommendations           │  │
│  │  /ml_recommend     - ML-based food suggestions            │  │
│  │  /generate_report  - Create user reports                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────┬────────────────┬────────────────┬────────────────────────┘
      │                │                │
      │                │                │
      ▼                ▼                ▼
┌──────────┐   ┌────────────┐   ┌──────────────────┐
│ Database │   │ AI Engine  │   │   ML Models      │
│ Module   │   │  Module    │   │    Module        │
│ (db.py)  │   │(ai_engine  │   │  (ml_model.py)   │
│          │   │   .py)     │   │                  │
└────┬─────┘   └──────┬─────┘   └────────┬─────────┘
     │                │                   │
     │                │                   │
     ▼                │                   │
┌─────────────────────┐                  │
│  PostgreSQL DATABASE    │                  │
│                     │                  │
│  ┌───────────────┐  │                  │
│  │   TABLES      │  │                  │
│  ├───────────────┤  │                  │
│  │ • USERS       │  │                  │
│  │ • GOALS       │  │                  │
│  │ • MEALS       │  │                  │
│  │ • ACTIVITIES  │  │                  │
│  │ • DAILY_LOG   │  │                  │
│  │ • MEAL_LOG    │  │                  │
│  │ • ACTIVITY_LOG│  │                  │
│  │ • SUGGESTIONS │  │                  │
│  │ • REPORTS     │  │                  │
│  │ • MOOD_LOG    │  │                  │
│  └───────────────┘  │                  │
│                     │                  │
│  ┌───────────────┐  │                  │
│  │ DB FEATURES   │  │                  │
│  ├───────────────┤  │                  │
│  │ • Triggers    │  │                  │
│  │ • Procedures  │  │                  │
│  │ • Functions   │  │                  │
│  │ • Indexes     │  │                  │
│  │ • Security    │  │                  │
│  └───────────────┘  │                  │
└─────────────────────┘                  │
                                         │
     ┌───────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│          CLASSICAL AI CONCEPTS                   │
│          (ai_engine.py - 920 lines)              │
│                                                  │
│  1. Intelligent Agent (DietAdvisorAgent)        │
│  2. State Space (Health states)                 │
│  3. Search Algorithms (BFS, DFS, A*)            │
│  4. Reasoning (Forward, Backward, Abductive)    │
│  5. Fuzzy Logic (Calorie classification)        │
│  6. Semantic Networks (Knowledge graph)         │
│  7. Frame Systems (Structured data)             │
│  8. STRIPS Planning (Goal-based planning)       │
│  9. Expert System (Rule-based decisions)        │
│ 10. Probabilistic Reasoning (Bayesian)          │
│ 11. Production System (IF-THEN rules)           │
│ 12. Knowledge Representation                    │
└─────────────────────────────────────────────────┘

     ┌───────────────────────────────────────────┐
     │                                           │
     ▼                                           ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  MACHINE LEARNING       │     │  DATA MINING PROJECT    │
│  (ml_model.py)          │     │  (data_mining_project/) │
│                         │     │                         │
│ • Random Forest Model   │     │ • Training notebooks    │
│ • Feature Scaling       │     │ • Nutritional dataset   │
│ • Label Encoding        │     │ • Model artifacts       │
│ • Prediction Pipeline   │     │ • Data preprocessing    │
│                         │     │                         │
│ Models loaded:          │     │ Location:               │
│ • diet_model.pkl        │     │ flask_app/models/       │
│ • scaler.pkl            │     │                         │
│ • category_encoder.pkl  │     │                         │
│ • measure_encoder.pkl   │     │                         │
│ • feature_names.pkl     │     │                         │
└─────────────────────────┘     └─────────────────────────┘
```

---

## 🔄 Data Flow Examples

### Example 1: User Login
```
1. User enters credentials in browser
2. POST /login → flask_app/app.py
3. authenticate_user() called
4. execute_query() → db.py
5. Query PostgreSQL DB (USERS table)
6. Return user data if valid
7. Create session
8. Redirect to /user_dashboard
```

### Example 2: Get AI Recommendation
```
1. User clicks "Get AI Recommendation"
2. POST /get_recommendation → flask_app/app.py
3. get_ai_recommendation() called → ai_engine.py
4. DietAdvisorAgent initialized
5. Perceive user data (calories, BMI, goals)
6. Run search algorithms (BFS/DFS/A*)
7. Apply fuzzy logic for calorie classification
8. Use reasoning engine (forward/backward reasoning)
9. Generate recommendation text
10. Return to user dashboard
11. Display recommendation
```

### Example 3: ML Food Recommendation
```
1. User enters nutritional goals (calories, protein, etc.)
2. POST /ml_recommend → flask_app/app.py
3. ml_model.recommend() called → ml_model.py
4. Load trained models (pkl files)
5. Prepare features from user input
6. Scale features using StandardScaler
7. Predict using Random Forest
8. Decode labels (food categories)
9. Return top 5 food recommendations
10. Display in user dashboard
```

### Example 4: Log Daily Meal
```
1. User selects meal and quantity
2. POST /log_meal → flask_app/app.py
3. log_meal() called
4. execute_query() → db.py
5. INSERT into MEAL_LOG table
6. PostgreSQL trigger activated automatically
7. Trigger updates DAILY_LOG table (total calories)
8. Trigger checks if goal met
9. Success message returned
10. Dashboard refreshed with new data
```

---

## 📂 File Structure Visual

```
SmartDietPlanner/
│
├── 📱 FRONTEND (Web UI)
│   └── flask_app/
│       ├── templates/
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── user_dashboard.html
│       │   └── admin_dashboard.html
│       └── static/
│           └── style.css
│
├── 🔧 BACKEND (Logic)
│   └── flask_app/
│       ├── app.py              # Main application (1661 lines)
│       ├── db.py               # Database utilities
│       └── ml_model.py         # ML model loader (226 lines)
│
├── 🧠 AI ENGINE
│   └── ai_engine.py            # Classical AI (920 lines)
│
├── 🤖 MACHINE LEARNING
│   └── data_mining_project/
│       ├── ml_inference.py     # Extended ML system
│       ├── models/             # Trained models (pkl files)
│       ├── data/               # Nutritional dataset
│       └── notebooks/          # Jupyter notebooks
│
├── 🗄️ DATABASE
│   └── database/
│       ├── create_tables.sql
│       ├── procedures.sql
│       ├── triggers.sql
│       ├── functions.sql
│       └── ... (other SQL files)
│
├── 📚 DOCUMENTATION
│   ├── ARCHITECTURE.md         # This file
│   ├── QUICK_START.md          # Quick start guide
│   ├── CLEANUP_SUMMARY.md      # Cleanup report
│   ├── AI_MODULE_DOCUMENTATION.md
│   └── README.md
│
└── 🛠️ UTILITIES
    └── utils/
        ├── constants.py
        ├── helpers.py
        └── validators.py
```

---

## 🎯 Integration Points

### 1. Flask ↔ Database
- **File**: `flask_app/db.py`
- **Function**: `get_db_connection()`, `execute_query()`
- **Connection**: psycopg2 library
- **Pool**: Connection pooling enabled

### 2. Flask ↔ AI Engine
- **Import**: `from ai_engine import get_ai_recommendation`
- **Called from**: `/get_recommendation` route
- **Input**: User data (calories, BMI, goals, activity)
- **Output**: AI-generated recommendation text

### 3. Flask ↔ ML Model
- **Import**: `from ml_model import ml_model`
- **Called from**: `/ml_recommend` route
- **Input**: Nutritional goals (calories, protein, carbs, fats)
- **Output**: List of recommended foods

### 4. Database ↔ Triggers
- **Automatic**: Triggers fire on INSERT/UPDATE/DELETE
- **Example**: `MEAL_LOG` insert → Trigger updates `DAILY_LOG`
- **No code needed**: Database handles automatically

---

## 🔐 Security Features

```
┌─────────────────────────────────────┐
│        Authentication               │
│  • Password hashing in DB           │
│  • Session management (Flask)       │
│  • Login required decorators        │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│        Authorization                │
│  • User roles (Admin, User)         │
│  • Role-based access control        │
│  • Admin-only routes                │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│        Database Security            │
│  • SQL injection prevention         │
│  • Parameterized queries            │
│  • Connection pooling               │
│  • Error handling                   │
└─────────────────────────────────────┘
```

---

## 📊 Technology Stack

```
┌──────────────────────────────────────────────┐
│              FRONTEND                         │
│  • HTML5                                      │
│  • CSS3 (Custom styling)                      │
│  • JavaScript (Vanilla)                       │
│  • Jinja2 Templates                           │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│              BACKEND                          │
│  • Python 3.x                                 │
│  • Flask (Web framework)                      │
│  • psycopg2 (Database driver)                 │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│              AI/ML                            │
│  • NumPy (Numerical computing)                │
│  • Scikit-learn (ML models)                   │
│  • Joblib (Model persistence)                 │
│  • Custom AI algorithms                       │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│              DATABASE                         │
│  • PostgreSQL Database 21c XE                     │
│  • PL/SQL (Procedures, Functions, Triggers)   │
│  • SQL (Queries, DDL, DML)                    │
└──────────────────────────────────────────────┘
```

---

## 🎓 For Academic Presentation

### Slide 1: Architecture Overview
- Show the main system diagram
- Explain: Frontend → Backend → AI/ML → Database

### Slide 2: Flask Application
- Entry point: `flask_app/app.py`
- Routes: Login, Dashboard, Logging, Recommendations
- Templates: HTML + CSS

### Slide 3: Classical AI Integration
- `ai_engine.py` - 920 lines, 12 AI concepts
- Live demo: Get AI Recommendation button
- Show search tree visualization

### Slide 4: Machine Learning
- `ml_model.py` - Random Forest model
- Trained on nutritional data
- Live demo: ML food recommendations

### Slide 5: Database Features
- PostgreSQL DB with 10+ tables
- Triggers (auto-update daily logs)
- Procedures (report generation)
- Functions (BMI calculation)

### Slide 6: Integration Success
- All components work together
- Clean architecture
- Production-ready code

---

## ✅ Verification Checklist

- [x] Application starts without errors
- [x] Login page loads correctly
- [x] Database connection works
- [x] AI engine initializes
- [x] ML models load successfully
- [x] Routes respond correctly
- [x] Sessions work properly
- [x] Templates render correctly
- [x] No broken imports
- [x] Clean code structure

---

## 🚀 Current Status

**Application Status**: ✅ RUNNING
**URL**: http://127.0.0.1:3001
**AI Engine**: ✅ INITIALIZED
**Database**: ✅ CONNECTED
**ML Models**: ✅ LOADED

**Result**: 🎉 Production Ready!
