# 🚀 Quick Start: Testing the New Smart Goal Page

## 1. Start the Flask Server

```bash
cd flask_app
python app.py
```

Server should run on: `http://127.0.0.1:4001`

---

## 2. Access the New Goal Page

1. Open browser: http://localhost:4001 (or http://127.0.0.1:4001)
2. Login with your test credentials
3. Navigate to: **Goals** section → **"Add New Goal"** button
4. Or direct URL: `/user/add-goal`

---

## 3. Test New Features (In Order)

### ✅ Feature 1: Selection Cards
- See 4 goal cards with emojis: 📉 📈 ⚖️ 💪
- Click each one - notice the blue highlight & background change
- This replaces the old dropdown!

### ✅ Feature 2: Current Weight Auto-Fill
- Look at "Current Weight" field
- It should show your profile weight (e.g., "70 kg")
- You can still edit it if needed

### ✅ Feature 3: Goal Speed Selection
- See 3 speed cards: 🐢 🏃 ⚡
- Each shows weekly rate (0.5 / 0.75 / 1 kg/week)
- Each shows calorie impact (-300 / -500 / -700 kcal)
- Select "Moderate" (should be selected by default)

### ✅ Feature 4: Live Calculations
- Enter Target Weight: 65 kg
- **Immediately see:**
  - Estimated Duration: 10 weeks (for Slow) or 7 weeks (for Moderate)
  - Suggested Date: automatically calculated (Today + weeks)
  - Daily Calorie Target: ~1,825 kcal (updates with speed changes)
  - Smart Tip: changes based on your selections

### ✅ Feature 5: Goal Summary Panel (Right Sidebar)
- Watch it update as you change selections
- Shows:
  - Goal Type
  - Weight Change (with emoji arrow ↑ or ↓)
  - Estimated Duration
  - Goal Speed
  - Daily Calorie Target (highlighted in red)
  - Smart dynamic tip
  - Timeline visualization (progress bar)

### ✅ Feature 6: Validation Feedback
- Try setting Target Weight = 70 kg (same as current)
- Select "Weight Loss"
- Should show error: ⚠️ "Target weight must be lower..."
- Try entering past date
- Should show error: ⚠️ "Target date must be in the future..."

### ✅ Feature 7: Submit Goal
- Fill in all fields correctly:
  - Goal Type: "Lose Weight" (📉 card)
  - Current Weight: 70 kg
  - Target Weight: 65 kg
  - Goal Speed: "Moderate" (🏃 card)
  - Target Date: Pick any future date (or use suggested)
- Click "Create Goal"
- Should redirect to Goals page with success message

---

## 4. Verify It Saved

After submitting:
1. Go back to Profile/Goals page
2. Should see your new goal listed
3. It should show the goal speed you selected
4. Weight range should be correct (70 → 65 kg)

---

## 5. Test Update (Edit Existing Goal)

1. Go back to `/user/add-goal`
2. Form should show your **previous goal values pre-filled**
3. Note the message: "You can only have one active goal. Updating..."
4. Change something: try selecting "Aggressive" speed
5. Submit
6. Should update (not create duplicate)

---

## 6. Test All Speed Options

### Slow & Healthy (🐢)
- Current: 70 kg → Target: 65 kg
- Weekly rate: 0.5 kg
- **Estimated weeks: 10**
- Calorie adjustment: -300 kcal
- Tip should mention: "For sustainable... 0.5-1 kg per week..."

### Moderate (🏃)  [Default]
- Same inputs
- Weekly rate: 0.75 kg
- **Estimated weeks: 7**
- Calorie adjustment: -500 kcal
- Tip should mention: "Balanced approach... 500 kcal deficit..."

### Aggressive (⚡)
- Same inputs
- Weekly rate: 1 kg
- **Estimated weeks: 5**
- Calorie adjustment: -700 kcal
- Tip should mention: "⚠️ Be careful... aggressive..."

---

## 7. Test Different Goal Types

### Weight Loss (📉)
- Validate: Target must be < Current
- Example: Current 70 → Target 65 ✅
- Example: Current 70 → Target 75 ❌ (error)

### Weight Gain (📈)
- Validate: Target must be > Current
- Example: Current 70 → Target 75 ✅
- Example: Current 70 → Target 60 ❌ (error)

### Maintain Weight (⚖️)
- Validate: Target should be ≈ Current (within 2 kg)
- Example: Current 70 → Target 71 ✅
- Example: Current 70 → Target 80 ⚠️ (warning)

### Fitness (💪)
- Validate: Any weights okay (fitness not about weight)
- No special validation

---

## 8. Browser Console Check

Open Browser Dev Tools (F12):
1. Go to **Console** tab
2. There should be **NO errors** (no red messages)
3. Select goal speed - should see no JavaScript errors
4. Submit form - should see no network errors

---

## 9. Database Check (Optional)

If you want to verify it saved with goal_speed:

```sql
-- In SQL*Plus or SQL Developer
SELECT goal_id, goal_type, goal_speed, target_value, current_value 
FROM GOALS 
WHERE user_id = 1
ORDER BY created_date DESC
FETCH FIRST 1 ROWS ONLY;
```

Should show:
```
GOAL_ID  GOAL_TYPE      GOAL_SPEED    TARGET_VALUE  CURRENT_VALUE
---      Weight Loss    Moderate      65            70
```

If `goal_speed` column doesn't exist, you'll get an error - that's okay! 
The app gracefully handles it and will still work.

---

## 10. Optional: Add goal_speed Column to Database

If you want the goal_speed to persist in the database:

### Option A: Python Script
```bash
cd SmartDietPlanner
python migrate_goal_speed.py
```

### Option B: SQL Direct
```sql
ALTER TABLE GOALS ADD (
    goal_speed VARCHAR(20) DEFAULT 'Moderate' 
    CHECK (goal_speed IN ('Slow & Healthy', 'Moderate', 'Aggressive'))
);
```

### Option C: Don't migrate
- App still works fine without it
- goal_speed will work on this session only
- Defaults to 'Moderate' if column missing

---

## Expected Behavior Summary

| Action | Expected Result |
|--------|-----------------|
| Visit page | See 4 goal cards + 3 speed cards |
| Enter weight | See timeline auto-calculate |
| Change speed | See calorie target update + weeks change |
| Change goal type | See tips update + validation rules change |
| Enter past date | See error message |
| Submit form | Redirect to goals page + success message |
| Return to page | Form shows previous values pre-filled |

---

## Troubleshooting

### ❌ "Page shows blank" or "No form"
- Hard refresh: Ctrl+F5
- Clear browser cache
- Check Flask server is running (watch for errors)

### ❌ "Selection cards don't highlight"
- Check browser supports CSS (all modern browsers do)
- Look for console errors (F12 → Console)

### ❌ "Calculations not updating"
- Check JavaScript isn't disabled
- F12 → Console, should see no errors
- Try refreshing page

### ❌ "Form won't submit"
- Check all required fields are filled
- Look for validation error messages
- Check browser console for errors

### ❌ "Date field won't accept today's date"
- System requires FUTURE date (at least tomorrow)
- Click "Suggested Date" button instead
- Or manually pick tomorrow's date

### ❌ "Database error when submitting"
- Check server logs for detailed error
- If "goal_speed doesn't exist" - try migration
- Database connection might be broken

---

## Performance Notes

- ✅ Real-time calculations: Instant (JavaScript)
- ✅ Page load: < 2 seconds
- ✅ Form submission: < 1 second (depends on DB)
- ✅ No lag when changing selections

---

## Success Indicators ✅

You'll know it's working when you see:

1. ✅ Selection cards with color changes
2. ✅ Speed cards showing weekly rates & calories
3. ✅ Current weight pre-filled
4. ✅ Timeline updates as you type
5. ✅ Suggested date appears automatically
6. ✅ Calorie target shows as ~number kcal
7. ✅ Tips change based on your selections
8. ✅ Summary card updates in real-time
9. ✅ Goal saves successfully
10. ✅ No errors in browser console

---

**🎯 That's it! You're now testing the Smart Goal Planner! 🚀**

If everything works, congratulations - the most intelligent goal-setting experience is ready!
