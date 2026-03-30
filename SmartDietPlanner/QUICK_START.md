# 🚀 Quick Start Guide - Smart Diet Planner

## Clean Architecture ✅
The project has been cleaned up! Only essential files remain.

---

## 📁 Current Project Structure
```
SmartDietPlanner/
├── flask_app/              # Main web application
├── ai_engine.py            # Classical AI module
├── data_mining_project/    # ML models
├── database/               # SQL scripts
├── utils/                  # Utilities (optional)
├── ARCHITECTURE.md         # Detailed architecture doc
└── README.md
```

---

## 🎯 How to Run the Project

### Step 1: Start Flask Application
```bash
cd flask_app
start.bat
```

**Or manually:**
```bash
cd flask_app
pip install -r requirements.txt
python app.py
```

### Step 2: Access Application
Open browser: **http://localhost:5000**

---

## 👤 Login Credentials

### Admin Account
- Username: `zainab_moazzam`
- Password: (check your database)

### Test User
- Username: `test_user1`
- Password: (check your database)

---

## 🔍 Application Features

### User Dashboard
1. **Daily Logging**
   - Log meals
   - Log activities
   - Track calories

2. **AI Recommendations**
   - Classical AI suggestions
   - ML-based food recommendations

3. **Reports & Analytics**
   - View progress
   - Generate reports

### Admin Dashboard
1. **User Management**
2. **Database Statistics**
3. **System Overview**

---

## 🧠 AI/ML Integration

### Classical AI (ai_engine.py)
- Intelligent Agent
- Search Algorithms (BFS, DFS, A*)
- Reasoning Systems
- Fuzzy Logic
- Semantic Networks
- Expert System

### Machine Learning (ml_model.py)
- Random Forest Model
- Food Recommendations
- Nutritional Analysis

---

## 🗄️ Database Setup

1. **Import SQL files from `database/` folder:**
   ```sql
   @create_tables.sql
   @procedures.sql
   @triggers.sql
   @functions.sql
   @insert_data.sql
   ```

2. **Or use the complete setup:**
   ```sql
   -- Run all scripts in order
   ```

---

## 📊 Application Flow

```
Browser
  ↓
Flask App (flask_app/app.py)
  ├→ Database (db.py) → PostgreSQL DB
  ├→ AI Engine (ai_engine.py) → Classical AI Recommendations
  └→ ML Model (ml_model.py) → ML Recommendations
```

---

## 🛠️ Troubleshooting

### Database Connection Issues
- Check PostgreSQL database is running
- Verify credentials in `flask_app/db.py`
- Test connection: `python flask_app/db.py`

### ML Models Not Loading
- Ensure models exist in `flask_app/models/`
- Check: `diet_model.pkl`, `scaler.pkl`, etc.

### Port Already in Use
- Change port in `flask_app/app.py`
- Default: 5000

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `flask_app/app.py` | Main Flask application (all routes) |
| `flask_app/db.py` | Database connection utilities |
| `flask_app/ml_model.py` | ML model loader |
| `ai_engine.py` | Classical AI module |
| `ARCHITECTURE.md` | Detailed architecture documentation |

---

## ✅ Removed Unused Files

The following were removed to clean up architecture:
- ❌ `presentation/` - Unused Tkinter GUI
- ❌ `business/` - Unused business logic layer
- ❌ `data_access/` - Unused DAO layer
- ❌ `fastapi_app/` - Unused FastAPI alternative
- ❌ `react_frontend/` - Unused React frontend
- ❌ Test scripts (check_*, test_*, verify_*, etc.)
- ❌ `main.py` - Old entry point

---

## 🎓 For Presentation/Demo

1. **Show Login** → User/Admin authentication
2. **User Dashboard** → Daily logging, AI recommendations
3. **Admin Dashboard** → System statistics, user management
4. **AI Module** → Explain classical AI concepts in `ai_engine.py`
5. **ML Module** → Show food recommendations from ML model
6. **Database** → Demonstrate triggers, procedures, functions

---

## 📞 Support

For issues or questions:
1. Check `ARCHITECTURE.md` for detailed architecture
2. Review `flask_app/README.md` for Flask-specific info
3. See `AI_MODULE_DOCUMENTATION.md` for AI concepts

---

## 🎉 Ready to Present!

Your project now has a clean, professional architecture with:
- ✅ Single entry point (Flask app)
- ✅ Clear file structure
- ✅ Integrated AI + ML + Database
- ✅ Full documentation
