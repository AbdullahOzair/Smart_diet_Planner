# ML Diet Recommendation - Setup Guide

## ✅ What I've Done

I've integrated **ML-powered diet recommendations** directly into your **Flask app** (not React - that was my mistake!). Now when users set goals, they get AI recommendations using your existing app theme.

## 📁 Files Created/Modified

### NEW FILES:
1. **flask_app/ml_model.py** - ML inference module that loads models and generates recommendations
2. **flask_app/models/** - Directory for trained model pickle files (will be created when you export)

### MODIFIED FILES:
1. **flask_app/app.py** - Added `/user/get-recommendation` API route
2. **flask_app/templates/user_dashboard.html** - Added AI recommendation card in goals view
3. **data_mining_project/notebooks/phase1_data_loading.ipynb** - Added model export cell

## 🎯 How It Works

1. User goes to "My Goals" page in your Flask app
2. Clicks "Get Recommendation" button
3. AI analyzes their goal (Weight Loss/Gain/etc.)
4. Shows:
   - Food category to focus on (Fruits, Vegetables, Protein, etc.)
   - Confidence percentage
   - Personalized nutrition advice
   - Recommended calories, protein, carbs per meal
5. Saves recommendation to SUGGESTIONS table

## ⚙️ Setup Steps (TO DO)

### Step 1: Export Trained Models from Notebook

**Run this in your Jupyter notebook:**

```python
# Open: data_mining_project/notebooks/phase1_data_loading.ipynb
# Find the last cell (added by me) titled "📦 Step 1: Export Models"
# Run ALL cells in order from top to bottom
# Then run the export cell - it will create flask_app/models/ folder with .pkl files
```

The export cell will create:
- diet_model.pkl
- scaler.pkl
- label_encoder_food.pkl
- label_encoder_measure.pkl
- label_encoder_category.pkl
- feature_columns.pkl

**IMPORTANT**: You must re-run the notebook cells that define `tuned_model`, `scaler`, and `label_encoders` before running the export cell.

### Step 2: Verify Flask App

Your Flask app is **already running** on http://localhost:3001

If you stopped it, restart with:
```powershell
cd "d:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app"
& "D:/7th semester/merge semester project/Smart_diet_Planner/SmartDietPlanner/venv/Scripts/python.exe" app.py
```

### Step 3: Test the Integration

1. Open http://localhost:3001 in your browser
2. Login with your credentials
3. Go to "My Goals" (sidebar)
4. If you have goals, you'll see **"AI-Powered Diet Recommendations"** card
5. Click **"Get Recommendation"** button
6. Wait for AI to analyze (shows loading spinner)
7. See personalized recommendation with:
   - Food category emoji 🍎
   - Recommendation text
   - Nutrition breakdown
   - Confidence score

## 🎨 Theme Integration

The recommendation card uses **your exact theme**:
- **Burnt Orange accent** (#C2410C, #EA580C)
- **Charcoal dark background** (#1C1917, #292524)
- **Stone text colors** (#F5F5F4, #D6D3D1)
- **Bootstrap Icons** (bi-robot, bi-stars)
- **Your existing button styles**
- **Gradient effects** matching admin dashboard

## 🗄️ Database Integration

Recommendations are automatically saved to:
```sql
INSERT INTO SUGGESTIONS (user_id, suggestion_type, suggestion_text, created_date)
VALUES (:user_id, 'ML Diet Recommendation', :suggestion_text, SYSDATE)
```

## ❓ Troubleshooting

### "ML models not available" error:
- You need to export models from notebook first (Step 1 above)
- Check if `flask_app/models/` folder exists with .pkl files

### Recommendation not showing:
- Make sure you have at least one goal created
- The recommendation card only appears when `goals` exist

### JavaScript errors:
- Check browser console (F12)
- Make sure Flask app is running on port 3001

## 🚀 Next Steps (Optional Enhancements)

1. **Auto-refresh**: Show recommendation when goal is created
2. **Multiple goals**: Let user select which goal to analyze
3. **History**: Show past recommendations
4. **Food database**: Link to actual food items from your database

## 💡 Key Difference from React Version

- **React version** (I made by mistake): Separate frontend, needs `npm start`, runs on port 3000
- **Flask version** (what you actually need): Built into your existing app, uses your templates, runs on port 3001

You can **delete** the `react_frontend` and `fastapi_app` folders - you don't need them!

---

**Your app is now ready!** Just export the models from the notebook and test the recommendation feature.
