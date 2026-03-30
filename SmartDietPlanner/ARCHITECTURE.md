# Smart Diet Planner - Architecture Documentation

## 🏗️ Clean Architecture Overview

### Active Application Stack
- **Frontend**: Flask Web Application
- **Backend**: Flask + PostgreSQL Database
- **AI/ML**: AI Engine (Classical AI) + ML Models
- **Database**: PostgreSQL Database (with triggers, procedures, functions)

---

## 📁 Project Structure (After Cleanup)

```
SmartDietPlanner/
├── flask_app/                    # ✅ ACTIVE - Web Application
│   ├── app.py                    # Main Flask application with all routes
│   ├── db.py                     # Database connection utilities
│   ├── ml_model.py              # ML model loader and inference
│   ├── start.bat                # Quick start script
│   ├── requirements.txt         # Python dependencies
│   ├── templates/               # HTML templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── user_dashboard.html
│   │   └── admin_dashboard.html
│   └── static/                  # CSS and static assets
│       └── style.css
│
├── ai_engine.py                 # ✅ ACTIVE - Classical AI Module
│                                # (Agent, Search, Reasoning, Fuzzy Logic)
│
├── data_mining_project/         # ✅ ACTIVE - ML Models
│   ├── ml_inference.py         # ML inference module (optional, not directly used)
│   ├── models/                 # Trained ML models
│   │   ├── diet_model.pkl
│   │   ├── scaler.pkl
│   │   ├── category_encoder.pkl
│   │   ├── measure_encoder.pkl
│   │   └── feature_names.pkl
│   ├── data/
│   │   └── nutrients_csvfile.csv
│   └── notebooks/
│       └── phase1_data_loading.ipynb
│
├── database/                    # ✅ ACTIVE - Database Scripts
│   ├── create_tables.sql
│   ├── procedures.sql
│   ├── triggers.sql
│   ├── functions.sql
│   └── ... (other SQL files)
│
├── utils/                       # ⚠️ UNUSED but kept for future
│   ├── constants.py
│   ├── helpers.py
│   └── validators.py
│
├── main.py                      # ⚠️ UNUSED - Old entry point
├── requirements.txt             # ✅ Root dependencies
└── README.md

REMOVED FOLDERS (Not Used):
├── presentation/                # ❌ Tkinter GUI (commented out, not used)
├── business/                    # ❌ Unused business logic layer
├── data_access/                 # ❌ Unused DAO layer
├── fastapi_app/                 # ❌ Alternative API (not used)
└── react_frontend/              # ❌ Alternative frontend (not used)
```

---

## 🔄 Application Flow

### 1. User Login/Registration Flow
```
Browser → Flask Route (/login or /register)
         → app.py: authenticate_user() or register_user()
         → db.py: execute_query()
         → PostgreSQL Database (USERS table)
         → Response to user
```

### 2. Dashboard Flow
```
Browser → Flask Route (/user_dashboard or /admin_dashboard)
         → app.py: get_user_data()
         → db.py: execute_query()
         → PostgreSQL Database (multiple tables)
         → Render template with data
```

### 3. AI Recommendation Flow
```
User Request → Flask Route (/get_recommendation)
             → app.py: calls get_ai_recommendation()
             → ai_engine.py: DietAdvisorAgent
                ├── State Space Search
                ├── BFS/DFS/A* Search
                ├── Fuzzy Logic
                ├── Reasoning Engine
                └── Returns recommendation
             → Display to user
```

### 4. ML Recommendation Flow
```
User Input → Flask Route (/ml_recommend)
           → app.py: calls ml_model.recommend()
           → ml_model.py: DietRecommendationModel
              ├── Load models from flask_app/models/
              ├── Prepare features
              ├── Make prediction
              └── Return food recommendations
           → Display to user
```

### 5. Daily Log Flow
```
User Logs Meal/Activity → Flask Route (/log_meal or /log_activity)
                        → app.py: log_meal() or log_activity()
                        → db.py: execute_query()
                        → PostgreSQL Database
                           ├── MEAL_LOG table
                           ├── ACTIVITY_LOG table
                           └── Triggers automatically update DAILY_LOG
                        → Success response
```

---

## 🗄️ Database Integration

### Active Tables
1. **USERS** - User profiles and authentication
2. **GOALS** - User fitness goals
3. **MEALS** - Available meal options
4. **ACTIVITIES** - Available activities
5. **DAILY_LOG** - Daily calorie tracking
6. **MEAL_LOG** - User meal entries
7. **ACTIVITY_LOG** - User activity entries
8. **SUGGESTIONS** - AI/ML recommendations
9. **REPORTS** - Generated reports
10. **MOOD_LOG** - User mood tracking

### Database Features Used
- ✅ **Triggers** - Automatic daily log updates
- ✅ **Procedures** - Complex operations (e.g., generate_user_report)
- ✅ **Functions** - Calculations (e.g., calculate_bmi)
- ✅ **Indexes** - Query optimization
- ✅ **Security** - User roles and permissions

---

## 🧠 AI/ML Components

### Classical AI (ai_engine.py)
1. **Intelligent Agent** - Diet Advisor Agent
2. **State Space** - Health state representation
3. **Search Algorithms** - BFS, DFS, A*
4. **Reasoning** - Forward, Backward, Abductive
5. **Fuzzy Logic** - Calorie level classification
6. **Semantic Networks** - Knowledge representation
7. **Frames** - Structured data
8. **Planning** - STRIPS-like planner
9. **Expert System** - Rule-based recommendations
10. **Probabilistic Reasoning** - Bayesian inference

### Machine Learning (ml_model.py)
1. **Random Forest Model** - Food recommendations
2. **Feature Scaling** - StandardScaler
3. **Label Encoding** - Category and measure encoding
4. **Prediction Pipeline** - End-to-end inference

---

## 🚀 How to Run

### Quick Start
```bash
cd flask_app
start.bat
```

### Manual Start
```bash
cd flask_app
pip install -r requirements.txt
python app.py
```

### Access Application
- URL: http://localhost:5000
- Admin: zainab_moazzam
- Test User: test_user1

---

## 📦 Dependencies

### Core Libraries
- Flask - Web framework
- psycopg2 - Database connectivity
- joblib - ML model loading
- numpy - Numerical operations

### Optional (for ML training)
- pandas - Data manipulation
- scikit-learn - ML models
- matplotlib - Visualization

---

## 🎓 Academic Integration

This project successfully integrates:
1. **Database Management** - PostgreSQL with advanced features
2. **Data Mining/Warehouse** - Structured nutritional data
3. **Classical AI** - 10+ AI concepts implemented
4. **Machine Learning** - Trained recommendation models
5. **Web Application** - Full-stack Flask application

---

## 📝 Key Files Explained

| File | Purpose | Status |
|------|---------|--------|
| `flask_app/app.py` | Main application with all routes (1661 lines) | ✅ Active |
| `flask_app/db.py` | Database utilities | ✅ Active |
| `flask_app/ml_model.py` | ML model integration | ✅ Active |
| `ai_engine.py` | Classical AI concepts (920 lines) | ✅ Active |
| `data_mining_project/ml_inference.py` | Extended ML system | ⚠️ Optional |
| `main.py` | Old entry point (mostly commented) | ❌ Can remove |
| `presentation/*` | Tkinter GUI (all commented) | ❌ Not used |
| `business/*` | Unused business layer | ❌ Not used |
| `data_access/*` | Unused DAO layer | ❌ Not used |
| `fastapi_app/*` | Alternative API | ❌ Not used |
| `react_frontend/*` | Alternative frontend | ❌ Not used |

---

## 🧹 Cleanup Recommendations

### Safe to Remove
1. ✅ `presentation/` folder - Unused Tkinter GUI
2. ✅ `business/` folder - Unused business logic
3. ✅ `data_access/` folder - Unused DAO layer
4. ✅ `fastapi_app/` folder - Unused FastAPI alternative
5. ✅ `react_frontend/` folder - Unused React alternative
6. ✅ Test scripts (check_*.py, test_*.py, verify_*.py, insert_*.py)
7. ✅ `main.py` - Old entry point (not used)

### Keep
1. ✅ `flask_app/` - Active application
2. ✅ `ai_engine.py` - Active AI module
3. ✅ `data_mining_project/` - ML models and notebooks
4. ✅ `database/` - SQL scripts
5. ✅ Documentation files (*.md)
6. ✅ `requirements.txt`

---

## 🎯 Summary

**Working Application**: Flask-based web application with PostgreSQL Database, Classical AI, and Machine Learning integration.

**Entry Point**: `flask_app/app.py` or `flask_app/start.bat`

**Clean Architecture**: Single frontend (Flask), single backend (Flask + PostgreSQL), AI module, ML models.
