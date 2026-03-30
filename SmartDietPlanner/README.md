# 🍎 Smart Diet & Lifestyle Planner

> An intelligent web application for personalized diet management, activity tracking, and AI-powered health recommendations

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-21c-red.svg)](https://www.postgresql.com/)

---

## 🎯 Overview

The Smart Diet & Lifestyle Planner is a comprehensive web application that integrates:
- **Database Management** - PostgreSQL with advanced features (triggers, procedures, functions)
- **Classical AI** - 12+ AI concepts including agents, search algorithms, reasoning, and fuzzy logic
- **Machine Learning** - Trained Random Forest models for food recommendations
- **Full-Stack Web App** - Flask-based responsive web application

**Perfect for academic projects demonstrating Database + AI + ML + Web Development integration.**

---

## ✨ Key Features

### 👤 User Features
- ✅ Secure authentication and registration
- ✅ Daily logging (meals, activities, water, sleep)
- ✅ Goal management and progress tracking
- ✅ AI-powered personalized recommendations
- ✅ ML-based food suggestions
- ✅ Comprehensive dashboard with analytics

### 👨‍💼 Admin Features
- ✅ User management and monitoring
- ✅ System statistics and metrics
- ✅ Content management (add meals/activities)
- ✅ Database overview and reports

---

## 📁 Project Structure

```
SmartDietPlanner/
│
├── 🧠 ai_module/                    # AI Engine (NEW Organized Folder)
│   ├── __init__.py                  # Package initializer
│   └── ai_engine.py                 # Classical AI (920 lines, 12 concepts)
│
├── 🌐 flask_app/                    # Web Application
│   ├── app.py                       # Main app (1661 lines, all routes)
│   ├── db.py                        # Database utilities
│   ├── ml_model.py                  # ML model loader (226 lines)
│   ├── requirements.txt             # Dependencies
│   ├── start.bat                    # Quick start script
│   ├── templates/                   # HTML templates
│   ├── static/                      # CSS and assets
│   └── models/                      # Trained ML models (pkl files)
│
├── 🤖 data_mining_project/          # ML Training & Data
│   ├── data/                        # Nutritional dataset (8000+ foods)
│   ├── notebooks/                   # Jupyter notebooks
│   └── ml_inference.py              # Extended ML system
│
├── 🗄️ database/                     # SQL Scripts
│   ├── create_tables.sql            # Table definitions
│   ├── procedures.sql               # Stored procedures
│   ├── triggers.sql                 # Database triggers
│   ├── functions.sql                # Database functions
│   └── ... (other SQL files)
│
└── 📚 Documentation/                # Guides and docs
    ├── AI_MODULE_DOCUMENTATION.md
    ├── ARCHITECTURE.md
    └── ... (other docs)
```

---

## 🚀 Quick Start

### Fastest Setup (Recommended)

```bash
setup_client.bat
flask_app\start.bat
```

This automatically recreates all tables in `XEPDB1`, creates triggers/functions/procedures, and seeds realistic demo data.

### 1. Setup Database

```bash
# Connect to PostgreSQL
sqlplus SYSTEM/your_password@localhost:1521/XEPDB1

# Run SQL scripts in order
@database/create_tables.sql
@database/insert_data.sql
@database/procedures.sql
@database/triggers.sql
@database/functions.sql
```

### 2. Configure Database Connection

Edit `flask_app/db.py`:
```python
DB_CONFIG = {
    'user': 'SYSTEM',
    'password': 'your_password',
    'dsn': 'localhost:1521/XEPDB1'
}
```

### 3. Install Dependencies

```bash
cd flask_app
pip install -r requirements.txt
```

### 4. Run Application

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
python app.py
```

### 5. Access Application

Open browser: **http://localhost:5000**

**Demo Credentials:**
- Admin: `zainab_moazzam`
- User: `test_user1`

---

## 🏗️ Architecture

```
Browser → Flask App → AI Module / ML Models / Database
          (app.py)    (ai_engine) (ml_model)  (PostgreSQL)
```

### Application Flow

1. **Login** → User authentication → Session creation
2. **Dashboard** → Display user data from database
3. **Log Activity** → Insert data → Triggers fire → Auto-update daily totals
4. **AI Recommendation** → Call ai_module → Classical AI processing → Return suggestion
5. **ML Suggestion** → Call ml_model → Load models → Predict → Return foods

---

## 🧠 AI/ML Integration

### Classical AI Module (ai_module/ai_engine.py)

**12 AI Concepts Implemented:**

1. **Intelligent Agent** - DietAdvisorAgent
2. **State Space** - Health state representation
3. **Search Algorithms** - BFS, DFS, A*
4. **Reasoning** - Forward, Backward, Abductive
5. **Fuzzy Logic** - Calorie classification
6. **Semantic Networks** - Knowledge graphs
7. **Frame Systems** - Structured data
8. **STRIPS Planning** - Goal-based planning
9. **Expert System** - Rule-based decisions
10. **Production System** - Pattern matching
11. **Probabilistic Reasoning** - Bayesian inference
12. **Knowledge Representation** - Multiple formats

### Machine Learning (flask_app/ml_model.py)

- **Model:** Random Forest Classifier
- **Training Data:** 8000+ food items
- **Features:** Calories, Protein, Fat, Carbs, Fiber
- **Output:** Top 5 food recommendations

---

## 🗄️ Database

### Tables (10 total)
- USERS, GOALS, MEALS, ACTIVITIES
- DAILY_LOG, MEAL_LOG, ACTIVITY_LOG
- SUGGESTIONS, REPORTS, MOOD_LOG

### Advanced Features
- ✅ **Triggers** - Auto-update daily logs
- ✅ **Procedures** - Report generation
- ✅ **Functions** - BMI calculation
- ✅ **Indexes** - Performance optimization
- ✅ **Security** - Role-based access

---

## 🔌 Main API Routes

### Authentication
- `GET /` - Home/Login page
- `POST /login` - Authenticate user
- `POST /register` - Create account
- `GET /logout` - Logout

### User Dashboard
- `GET /user_dashboard` - Main dashboard
- `POST /log_meal` - Log meal entry
- `POST /log_activity` - Log activity
- `GET /get_recommendation` - Get AI suggestion
- `POST /ml_recommend` - Get ML foods

### Admin Dashboard
- `GET /admin_dashboard` - Admin panel
- `POST /admin/add_meal` - Add meal to DB
- `POST /admin/add_activity` - Add activity

---

## ⚙️ Configuration

### Port Configuration
**Current Port:** 5000

**To change port**, edit `flask_app/app.py` (line 1660):
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

**Common alternative ports:** 8000, 8080, 3000, 5001

### Database Configuration
Edit `flask_app/db.py`:
```python
DB_CONFIG = {
    'user': 'YOUR_USERNAME',
    'password': 'YOUR_PASSWORD',
    'dsn': 'HOST:PORT/SERVICE'
}
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py to 8000, 8080, etc.
```

### Database Connection Error
1. Check PostgreSQL service is running
2. Verify credentials in `flask_app/db.py`
3. Test connection: `sqlplus SYSTEM/password@localhost:1521/XEPDB1`

### ML Models Not Loading
1. Ensure models exist in `flask_app/models/` directory
2. Files needed: `diet_model.pkl`, `scaler.pkl`, `category_encoder.pkl`, etc.
3. Train models using `data_mining_project/notebooks/phase1_data_loading.ipynb`

### Proxy Error
- Usually caused by port conflict
- Change port in `app.py` to an unused port (e.g., 8000)
- Check no other process is using the port

---

## 🧪 Testing

### Test Database Connection
```bash
cd flask_app
python -c "from db import get_db_connection; print(get_db_connection())"
```

### Test AI Module
```python
from ai_module.ai_engine import get_ai_recommendation

user_data = {
    'current_calories': 2200,
    'bmi': 25.5,
    'goal': 'lose_weight',
    'activity_level': 'moderate'
}

print(get_ai_recommendation(user_data))
```

### Test ML Model
```python
from flask_app.ml_model import ml_model

ml_model.load_models()
recommendations = ml_model.recommend(2000, 100, 250, 70)
print(recommendations)
```

---

## 📚 Documentation

- **[AI_MODULE_DOCUMENTATION.md](AI_MODULE_DOCUMENTATION.md)** - AI concepts explained
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete architecture
- **[VISUAL_ARCHITECTURE.md](VISUAL_ARCHITECTURE.md)** - Visual diagrams
- **[ML_INTEGRATION_GUIDE.md](ML_INTEGRATION_GUIDE.md)** - ML integration guide

---

## 🎓 Academic Features

This project demonstrates:

1. **Database Management (30%)**
   - PostgreSQL DB with 10+ tables
   - Triggers, procedures, functions
   - Complex queries and optimization

2. **Classical AI (25%)**
   - 12 AI concepts implemented
   - Agent-based system
   - Search and reasoning algorithms

3. **Machine Learning (25%)**
   - Data preprocessing and training
   - Model deployment and inference
   - Real-time predictions

4. **Full-Stack Development (20%)**
   - Flask web framework
   - RESTful API design
   - Responsive UI

---

## 📊 Project Statistics

- **Total Lines of Code:** 3000+
- **Python Files:** 15+
- **SQL Scripts:** 10+
- **AI Concepts:** 12
- **Database Tables:** 10
- **API Routes:** 25+

---

## 🎯 Project Status

✅ **Complete and Production-Ready**

- [x] Database implementation
- [x] AI module (organized in ai_module/ folder)
- [x] ML model training and integration
- [x] Web application development
- [x] Testing and debugging
- [x] Documentation
- [x] Ready for presentation/demo

---

## 🚀 Future Enhancements

- [ ] Mobile application
- [ ] Real-time notifications
- [ ] Social features
- [ ] Fitness wearable integration
- [ ] Advanced ML models (deep learning)
- [ ] Multi-language support

---

## 📞 Support

For issues or questions:
- Check documentation files
- Review troubleshooting section
- Test individual components

---

## 🎬 Demo Flow (For Presentation)

1. **Show Login** → User authentication
2. **User Dashboard** → Daily logging, stats
3. **AI Recommendation** → Click button, show AI output
4. **ML Food Suggestions** → Enter nutritional goals, get foods
5. **Admin Panel** → System statistics, user management
6. **Database** → Show triggers in action (log meal → auto-update)
7. **Code Walkthrough** → Explain AI concepts in `ai_module/ai_engine.py`

---

<div align="center">

**Made with ❤️ for Academic Excellence**

**Application Port: 5000** | **Database: PostgreSQL** | **Framework: Flask**

</div>
