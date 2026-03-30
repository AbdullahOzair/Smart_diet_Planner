# 🚀 Quick Reference Card

## Application Information

### Access
- **URL:** http://localhost:8080
- **Status:** ✅ Running
- **Port:** 8080 (changed from 3001)

### Login Credentials
- **Admin:** zainab_moazzam
- **User:** test_user1

---

## Port Configuration

### Current Port: 8080
**File:** `flask_app/app.py` (line 1660)
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Why Port 8080?
- Port 5000: ❌ Blocked by Windows
- Port 3001: ❌ Caused proxy errors
- Port 8080: ✅ Works perfectly

### Change Port
Edit `flask_app/app.py` line 1660 with your desired port

---

## Project Structure

```
SmartDietPlanner/
├── 🧠 ai_module/              # AI Engine (NEW organized folder)
├── 🌐 flask_app/              # Web Application
├── 🤖 data_mining_project/    # ML Models
├── 🗄️ database/               # SQL Scripts
├── 🛠️ utils/                  # Utilities
└── 📚 README.md               # Main documentation
```

---

## Key Changes Made

1. **Port Changed:** 3001 → 8080
2. **AI Organized:** ai_engine.py → ai_module/ai_engine.py
3. **READMEs Merged:** 3 READMEs → 1 comprehensive README
4. **Routes Fixed:** Updated imports in flask_app/app.py

---

## Quick Commands

### Start Application
```bash
cd flask_app
python app.py
```

### Access Application
```
http://localhost:8080
```

### Test Database
```bash
cd flask_app
python db.py
```

### Test AI Module
```python
from ai_module.ai_engine import get_ai_recommendation
```

---

## Project Features

### ✅ Organized Structure
- AI module in dedicated folder
- Similar to database/ and data_mining_project/
- Professional and clear

### ✅ Working Application
- Running on port 8080
- No proxy errors
- All routes functioning

### ✅ Complete Documentation
- Single comprehensive README
- AI module documentation
- Architecture documentation

---

## For Presentation

1. **Application:** http://localhost:8080
2. **Show Structure:** ai_module/, flask_app/, database/, data_mining_project/
3. **Demo AI:** Get AI Recommendation button
4. **Demo ML:** ML Food Suggestions
5. **Show Database:** Triggers in action
6. **Code Walkthrough:** ai_module/ai_engine.py

---

## Support

- **Main README:** Comprehensive guide
- **ARCHITECTURE.md:** Detailed architecture
- **REORGANIZATION_SUMMARY.md:** All changes explained

---

<div align="center">

**✅ PROJECT READY FOR DEMO**

**Status:** Running | **Port:** 8080 | **Structure:** Organized

</div>
