# 🎨 Visual Preview: Smart Goal Planner Page

## Overall Layout (Desktop View)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SmartDietPlanner                          [Profile] [Goals] [Dashboard]    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐  ┌──────────────┐
│                                                         │  │              │
│  Create Your Goal                                       │  │              │
│  ═════════════════════════════════════════════════      │  │ 📋 SUMMARY   │
│                                                         │  │ CARD         │
│  STEP 1: Choose Your Goal                              │  │ (sticky)     │
│  ┌───────────────────────────────────────────────────┐ │  │              │
│  │  📉 Lose      │  📈 Gain      │  ⚖️ Maintain  │    │  │ Goal: Weight │
│  │  Weight       │  Weight       │  Weight      │    │  │ Loss         │
│  └───────────────┴───────────────┴──────────────┴────┘ │  │              │
│  │  💪 Improve Fitness                         │      │  │ Change:      │
│  │  Get stronger & more active                │      │  │ 70 → 65 kg   │
│  └─────────────────────────────────────────┬──────┘  │  │ (↓5 kg)      │
│                                            │         │  │              │
│  STEP 2: Your Weight Details               │         │  │ Duration:    │
│  ┌─────────────────────────┬──────────────┐│         │  │ 10 weeks     │
│  │ Current: 70 kg (auto) ⓘ │ Target: __ kg││         │  │              │
│  │                         └──────────────┘│         │  │ Speed:       │
│  └─────────────────────────────────────────┘        │  │ Moderate     │
│                                                      │  │              │
│  STEP 3: How Fast?                                 │  │ ────────────  │
│  ┌──────────────┬──────────────┬─────────────┐     │  │              │
│  │ 🐢 SLOW      │ 🏃 MODERATE  │ ⚡AGGRESSIVE│     │  │ 🔥 Daily     │
│  │ 0.5 kg/week  │ 0.75/week ✓  │ 1 kg/week  │     │  │ Calorie:     │
│  │ -300 kcal    │ -500 kcal    │ -700 kcal  │     │  │ ~1,825 kcal  │
│  └──────────────┴──────────────┴─────────────┘     │  │              │
│                                                      │  │ 💡 Smart Tip:│
│  STEP 4: When to Reach It?                         │  │ "Balanced... │
│  ┌────────────────────┬──────────────────────────┐ │  │              │
│  │ Suggested: 15 May  │ Your Target: [calendar] │ │  │ Progress:    │
│  │ (10 weeks)         │                         │ │  │ ████░░░░░░  │
│  └────────────────────┴──────────────────────────┘ │  │              │
│                                                      │  │ 10 weeks away│
│  ┌──────────────────┬──────────────────────────┐   │  │              │
│  │ ✓ Create Goal    │ ✗ Cancel               │   │  └──────────────┘
│  └──────────────────┴──────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Step 1: Goal Selection (Shown First)

```
GOAL TYPE SELECTION
═══════════════════

 ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
 │   📉        │  │   📈        │  │   ⚖️        │  │   💪        │
 │             │  │             │  │             │  │             │
 │ Lose Weight │  │ Gain Weight │  │   Maintain  │  │  Improve    │
 │ Shed pounds │  │ Build muscle│  │  Weight     │  │  Fitness    │
 │‾‾‾‾‾‾‾‾‾‾‾‾‾  │             │  │             │  │             │
 │ & get healthier              │  │Stay at your │  │Get stronger │
 │             │  │             │  │ current     │  │ & more      │
 └─────────────┘  │ weight      │  │             │  │ active      │
                  │             │  │             │  │             │
                  └─────────────┘  └─────────────┘  └─────────────┘
                  
                  ✓ When clicked: Blue border + light blue background
                  ✓ Radio button hidden (modern UX)
                  ✓ Form remembers your choice
```

---

## Step 2: Weight Details (Auto-Filled)

```
WEIGHT DETAILS
══════════════

Current Weight (kg)          Target Weight (kg)
┌──────────────────────────┐  ┌──────────────────┐
│ 70 kg (auto-filled)      │  │ [Enter target]   │
│ ⓘ Your current weight    │  │ ⓘ Where you want │
│ from profile             │  │ to be            │
└──────────────────────────┘  └──────────────────┘

• ✓ Current auto-fills from user profile (profile[7])
• ✓ User can edit if needed (number input)
• ✓ Target is manual entry
• ✓ Both trigger validation when changed
```

---

## Step 3: Goal Speed Selection

```
GOAL SPEED - Choose Your Pace
══════════════════════════════

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│      🐢 SLOW     │  │    🏃 MODERATE   │  │    ⚡ AGGRESSIVE │
│   & Healthy      │  │                  │  │                  │
│                  │  │ ✓ SELECTED       │  │                  │
│  0.5 kg/week     │  │  0.75 kg/week    │  │  1 kg/week       │
│  -300 kcal       │  │  -500 kcal  ✓    │  │  -700 kcal       │
│                  │  │                  │  │                  │
│  Sustainable     │  │  Balanced time   │  │  Quick results   │
│  & healthy       │  │  & effort        │  │  but intense     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
                           ↑
                    Default selected
                    (but user can change)
```

---

## Step 4: Target Date (Smart Suggestion)

```
WHEN TO REACH IT?
═════════════════

Suggested Date                Your Target Date
┌──────────────────────────┐  ┌──────────────────────┐
│ 15 May 2026              │  │ [calendar picker]    │
│ Based on:                │  │ Can pick different   │
│ • Weight diff: 5 kg      │  │ date if preferred    │
│ • Speed: 0.75 kg/week    │  │                      │
│ • Calculated: 10 weeks   │  │ Validates to future  │
│ = Today + 70 days        │  │ date only            │
└──────────────────────────┘  └──────────────────┘
      ↓
  User can directly use suggestion
  or click to override
```

---

## Real-Time Summary Panel (Right Sidebar)

```
┌──────────────────────────────────────┐
│ 📋 GOAL SUMMARY - LIVE PREVIEW       │
├──────────────────────────────────────┤
│                                      │
│ Goal Type: Weight Loss               │
│ Weight Change: 70 → 65 kg (↓5 kg)   │
│ Estimated Duration: 10 weeks         │
│ Goal Speed: Moderate                 │
│ ─────────────────────────────────    │
│ 🔥 Daily Calorie Target              │
│ ┌──────────────────────────────────┐ │
│ │ ~1,825 kcal                      │ │
│ │ Based on goal & activity level   │ │
│ └──────────────────────────────────┘ │
│ ─────────────────────────────────    │
│ 💡 Smart Tip                         │
│ "Balanced approach: 500 kcal         │
│  deficit = 0.5 kg per week. Maintain │
│  with diet + light exercise."        │
│ ─────────────────────────────────    │
│ ◼◼◼◻◻◻◻◻◻◻ Timeline (30%)            │
│ 10 weeks away • Stay consistent!     │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │ ✓ Create Goal   ✗ Cancel        │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘

✓ Updates in REAL-TIME as user changes any field
✓ Shows exactly what their choices mean
✓ Sticky positioning (stays visible while scrolling)
```

---

## Real-Time Updates (What Changes When)

### When User Selects Goal Type:
```
[User clicks: 📉 Lose Weight]
  ↓
Summary updates:
  • Goal Type: "Weight Loss"
  • Tips change: "For weight loss..."
  • Validation: "Target must be < Current"
  
[User clicks: 💪 Improve Fitness]
  ↓
Summary updates:
  • Goal Type: "Improve Fitness"
  • Tips change: "Get fit: Focus on strength..."
  • Validation: "Any weights allowed"
```

### When User Enters Weight Values:
```
[User enters: Target 65 in the box]
  ↓
Calculations trigger:
  • Weight diff: 70 - 65 = 5 kg
  • Timeline: 5 ÷ 0.75 = 7 weeks (Moderate)
  • Suggested date: Today + 7 weeks
  • Progress bar: Updates to 30%
  
Summary updates to:
  • Weight Change: "70 → 65 kg (↓5 kg)"
  • Duration: "7 weeks"
  • Milestone text: "7 weeks away • Stay consistent!"
```

### When User Changes Speed:
```
[User clicks: ⚡ AGGRESSIVE -700 kcal]
  ↓
Calculations trigger:
  • Timeline recalculates: 5 ÷ 1.0 = 5 weeks
  • Suggested date advances: Today + 5 weeks
  • Calorie target recalculates: 2,325 - 700 = 1,625 kcal
  • Tips changes: "⚠️ Be careful: 700 kcal deficit..."
  
Summary updates to:
  • Goal Speed: "Aggressive"
  • Daily Calories: "~1,625 kcal"
  • Duration: "5 weeks"
  • Smart Tip: New warning message
  • Progress bar: Extends to show longer timeline
```

---

## Validation Feedback (Error Messages)

### When User Makes Invalid Choices:

```
Weight Loss Goal + Target >= Current Weight
┌─────────────────────────────────────────────────────┐
│ ⚠️ ERROR                                            │
│ Target weight must be lower than current weight     │
│ for weight loss goal                                │
│                                                     │
│ You entered: Current 70 → Target 75                 │
│ This is weight GAIN, not loss.                      │
│                                                     │
│ Fix: Set target < 70 kg                            │
└─────────────────────────────────────────────────────┘

Weight Gain Goal + Target <= Current Weight
┌─────────────────────────────────────────────────────┐
│ ⚠️ ERROR                                            │
│ Target weight must be higher than current weight    │
│ for weight gain goal                                │
│                                                     │
│ You entered: Current 70 → Target 65                 │
│ This is weight LOSS, not gain.                      │
│                                                     │
│ Fix: Set target > 70 kg                            │
└─────────────────────────────────────────────────────┘

Past Target Date
┌─────────────────────────────────────────────────────┐
│ ⚠️ ERROR                                            │
│ Target date must be in the future                   │
│ (at least tomorrow)                                 │
│                                                     │
│ You selected: 28 March 2026 (today)                │
│ Min allowed: 29 March 2026 (tomorrow)              │
│                                                     │
│ Fix: Pick 29 March 2026 or later                  │
└─────────────────────────────────────────────────────┘
```

---

## Success Flow (What Happens on Submit)

```
User fills form correctly:
  ✓ Goal Type: Weight Loss (📉)
  ✓ Current: 70 kg
  ✓ Target: 65 kg
  ✓ Speed: Moderate (🏃)
  ✓ Date: 15 May 2026 (future)

Clicks: "Create Goal"
  ↓
Backend validates all inputs
  ✓ All required fields filled
  ✓ No validation errors
  ✓ Date is future
  ✓ Weights are logical
  ↓
Goal saved to database
  ✓ Table: GOALS
  ✓ Columns: user_id, goal_type, current_value, target_value,
              target_date, goal_speed, start_date, status
  ✓ goal_speed saved: "Moderate"
  ↓
Redirects to: /user/goals page
  ↓
Success message shown:
"✓ Goal created successfully!"
  ↓
User sees new goal in their goals list:
"Weight Loss • 70 → 65 kg • Target: 15 May 2026
 Speed: Moderate • 10 weeks • Status: Active"
```

---

## Mobile View (Responsive)

```
On smaller screens (< 768px), layout stacks:

┌─────────────────────────────┐
│ Create Your Goal            │
├─────────────────────────────┤
│ [Goal Type Cards]           │  1 column
│ [Weight Fields]             │  full width
│ [Speed Cards]               │
│ [Date Fields]               │
│ [Buttons]                   │
├─────────────────────────────┤
│ [Summary Card]              │  Moves below
│ [Still sticky but full]     │
└─────────────────────────────┘

✓ Touch-friendly (larger targets)
✓ Cards stack vertically
✓ All features still work
✓ Summary card remains visible
```

---

## Interaction Timeline (First-Time User)

### Minute 0-5: Initial Page Load
1. User lands on `/user/add-goal`
2. Page loads with:
   - Empty form
   - 4 goal type cards (all unselected)
   - 3 speed cards (Moderate pre-selected ✓)
   - Current weight auto-filled: "70 kg"
   - Target weight empty
   - Summary card shows placeholders
   - Tips show generic message

### Minute 5-10: User Explores
1. User clicks 📉 "Lose Weight" card
   - Card highlights blue ✓
   - Summary updates: "Goal Type: Weight Loss"
   - Tips update to weight loss advice
2. User enters target weight: 65
   - Real-time calculation:
     • Timeline: "10 weeks"
     • Calories: "~1,825 kcal"
     • Suggested date: "15 May 2026"
   - Summary card fills in all details
3. User sees Moderate speed is default, keeps it
4. User accepts suggested date or picks custom

### Minute 10-15: User Submits
1. Clicks "Create Goal"
2. Backend validates (< 1 second)
3. Data saved to database
4. Redirects to Goals page
5. Success message shown: "✓ Goal created successfully!"

### Result: User sees realistic, achievable goal!

---

## Key Visual Elements

### Goal Cards (Unselected)
```
┌──────────────┐
│     📉       │
│              │
│ Lose Weight  │
│ Shed pounds  │
│ & get        │
│ healthier    │
└──────────────┘
Border: 2px solid #e9ecef (light gray)
Background: white
```

### Goal Cards (Selected ✓)
```
┌══════════════┐ ← Border: 2px solid #007bff (blue)
│     📉       │
│              │ ← Background: #f0f8ff (light blue)
│ Lose Weight  │
│ Shed pounds  │ ← Shadow: 0 0 0 3px rgba(0,123,255,0.1)
│ & get        │
│ healthier    │
└══════════════┘
```

### Speed Card Display
```
🐢 SLOW            🏃 MODERATE        ⚡ AGGRESSIVE
0.5 kg/week        0.75 kg/week       1 kg/week
-300 kcal          -500 kcal ✓        -700 kcal
```

### Calorie Display Box
```
┌────────────────────────────────┐
│ 🔥 Daily Calorie Target        │
│                                │
│       ~1,825 kcal              │ ← Large, bold, blue
│                                │
│ Based on your goal and         │ ← Explanation text
│ activity level                 │
└────────────────────────────────┘
```

---

## Color Scheme

| Element | Color | Hex | Purpose |
|---------|-------|-----|---------|
| Primary | Blue | #007bff | Main actions, selected state |
| Cards Unselected | Light Gray | #e9ecef | Inactive options |
| Cards Selected | Light Blue | #f0f8ff | Active selection |
| Calorie Alert | Warning Orange | #ff6b6b | Important number |
| Success | Green | #28a745 | Goal creation confirm |
| Error | Red | #dc3545 | Validation errors |
| Text | Dark Gray | #495057 | Body text |
| Border | Light Gray | #dee2e6 | Dividers |

---

## Summary Card Sticky Positioning

```
As user scrolls down the form:

[Form scrolls up ↑]
                                    
[Summary Card stays in viewport]    ← Sticky position (top: 20px)
[Always visible for reference]
                                    
Goal Summary
━━━━━━━━━
Goal Type: Weight Loss
Duration: 10 weeks
Speed: Moderate
🔥 ~1,825 kcal
───────────
Smart Tip: ...
```

---

**✨ That's what your users will see!**

**🚀 Modern, interactive, and intelligent goal planning!**
