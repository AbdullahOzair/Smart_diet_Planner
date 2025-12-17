# Pastel Wellness Theme - Quick Reference

## 🎨 Color Palette

### Primary Colors
```css
Tea Pink (Background):        #FAF3F0  ████████
Peach (Cards):                #FADADD  ████████
Dusty Rose (Primary Accent):  #E8B4BC  ████████
Sage (Secondary Accent):      #C8D8C0  ████████
```

### Text Colors
```css
Text Dark:                    #4A4A4A  ████████
Text Muted:                   #8A8A8A  ████████
```

### Supporting Colors
```css
Borders:                      #EDE0DD  ████████
Peach Light:                  #FCE8EB  ████████
Dusty Rose Dark:              #D89FA8  ████████
Sage Light:                   #D8E8D0  ████████
White:                        #FFFFFF  ████████
```

### Utility Colors (Soft Pastels)
```css
Danger (Soft Red):            #E8A4A4 → #D88888  ████████
Warning (Soft Orange):        #F4D4A8 → #E8C490  ████████
Info (Soft Blue):             #B4D4E8 → #A0C4D8  ████████
Success (Sage Green):         #C8D8C0 → #D8E8D0  ████████
```

## 🌈 Gradients

### Navbar & Headers
```css
background: linear-gradient(135deg, #E8B4BC 0%, #C8D8C0 100%);
/* Dusty Rose → Sage */
```

### Card Headers
```css
background: linear-gradient(135deg, #E8B4BC 0%, #FADADD 100%);
/* Dusty Rose → Peach */
```

### Sidebar
```css
background: linear-gradient(180deg, #FCE8EB 0%, #FFFFFF 100%);
/* Peach Light → White (vertical) */
```

### Stat Cards
```css
background: linear-gradient(135deg, #FFFFFF 0%, #FCE8EB 100%);
/* White → Peach Light */
```

### Active Nav Links
```css
background: linear-gradient(135deg, #E8B4BC 0%, #C8D8C0 100%);
/* Dusty Rose → Sage */
```

### Buttons
```css
/* Primary */
background: linear-gradient(135deg, #E8B4BC 0%, #D89FA8 100%);

/* Success */
background: linear-gradient(135deg, #C8D8C0 0%, #D8E8D0 100%);

/* Danger */
background: linear-gradient(135deg, #E8A4A4 0%, #D88888 100%);

/* Warning */
background: linear-gradient(135deg, #F4D4A8 0%, #E8C490 100%);

/* Info */
background: linear-gradient(135deg, #B4D4E8 0%, #A0C4D8 100%);
```

## 💫 3D Shadows

### Shadow Variables
```css
--shadow-sm:  0 2px 8px rgba(232, 180, 188, 0.1);
--shadow-md:  0 4px 12px rgba(232, 180, 188, 0.15);
--shadow-lg:  0 8px 24px rgba(232, 180, 188, 0.2);
--shadow-3d:  4px 4px 12px rgba(232, 180, 188, 0.15), 
              -2px -2px 8px rgba(255, 255, 255, 0.8);
```

### Usage
- **Cards**: `--shadow-3d` (dual-tone shadow)
- **Buttons**: `--shadow-sm` (subtle)
- **Modals**: `--shadow-lg` (prominent)
- **Navbar**: `--shadow-lg` (depth)
- **Hover Effects**: Increase shadow size by 50%

## 🔲 Border Radius

```css
Cards:              20px
Stat Cards:         18px
Buttons (Normal):   12px
Buttons (Small):    8px
Forms:              12px
Badges:             8px
Tables:             16px
Modals:             20px
Search Bar:         16px
Avatar (Circle):    50%
```

## 📐 Spacing

### Padding
```css
Card Body:          1.5rem (24px)
Card Header:        1.25rem 1.5rem (20px 24px)
Navbar:             1rem 2rem (16px 32px)
Sidebar:            2rem 0 (32px 0)
Nav Links:          0.875rem 1.5rem (14px 24px)
Buttons:            0.75rem 1.75rem (12px 28px)
Buttons (Small):    0.5rem 1rem (8px 16px)
Forms:              0.75rem 1rem (12px 16px)
```

### Margins
```css
Section Spacing:    2rem (32px)
Card Spacing:       1.5rem (24px)
Row Gap:            1.5rem (24px)
Form Groups:        1rem (16px)
```

## 🎯 Component Classes

### Cards
```html
<div class="card">                 /* Standard card */
<div class="stat-card">            /* Metric card with 3D effect */
<div class="login-card">           /* Login page card */
```

### Buttons
```html
<button class="btn btn-primary">   /* Dusty rose gradient */
<button class="btn btn-success">   /* Sage gradient */
<button class="btn btn-danger">    /* Soft red gradient */
<button class="btn btn-warning">   /* Soft orange gradient */
<button class="btn btn-info">      /* Soft blue gradient */
<button class="btn btn-sm">        /* Small size */
```

### Badges
```html
<span class="badge bg-primary">    /* Dusty rose */
<span class="badge bg-success">    /* Sage */
<span class="badge bg-danger">     /* Soft red */
<span class="badge bg-warning">    /* Soft orange */
<span class="badge bg-info">       /* Soft blue */
```

### Alerts
```html
<div class="alert alert-success">  /* Sage green */
<div class="alert alert-danger">   /* Soft red */
<div class="alert alert-info">     /* Soft blue */
<div class="alert alert-warning">  /* Soft orange */
```

### Special Components
```html
<div class="search-filter-bar">    /* Search/filter container */
<div class="user-avatar">          /* Circular avatar */
<div class="login-icon">           /* Login page icon */
<div class="stat-icon">            /* Metric icon box */
```

## 🎨 Design Principles

### 1. Soft & Welcoming
- Use pastel colors only
- Avoid high contrast
- Prefer gradients over solid colors
- Round all corners

### 2. Depth with 3D Effects
- Multi-layer shadows (highlight + shadow)
- Lift cards on hover
- Gradient backgrounds for depth
- White highlights for dimension

### 3. Wellness Aesthetic
- Health-related icons (heart, pulse, activity)
- Calming color palette
- Generous spacing (breathing room)
- Smooth animations

### 4. Consistency
- Use CSS variables for all colors
- Maintain shadow hierarchy
- Consistent border radius
- Uniform spacing scale

## 🖼️ Example Layouts

### Login Page
```
┌─────────────────────────────────────┐
│  Gradient Background (Tea Pink)     │
│  ┌───────────────────────────────┐  │
│  │  Gradient Header              │  │
│  │  (Dusty Rose → Sage)          │  │
│  │  ○ Icon (Heart Pulse)         │  │
│  │  Welcome Back                 │  │
│  ├───────────────────────────────┤  │
│  │  White Body                   │  │
│  │  [Username Input]             │  │
│  │  [Password Input]             │  │
│  │  [Sign In Button]             │  │
│  │  [Create Account Link]        │  │
│  │  Demo Credentials Box         │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Admin Dashboard
```
┌─────────────────────────────────────────────────────┐
│ Navbar (Gradient: Dusty Rose → Sage)                │
├────────┬────────────────────────────────────────────┤
│Sidebar │ Main Content                               │
│        │ ┌────────────────────┐ ┌────────────────┐ │
│• Dash  │ │ Stat Card (3D)     │ │ Stat Card (3D) │ │
│• Users │ │ ○ Icon             │ │ ○ Icon         │ │
│• Logs  │ │ 150 Users          │ │ 1,240 Logs     │ │
│• Goals │ └────────────────────┘ └────────────────┘ │
│        │                                            │
│        │ ┌──────────────────────────────────────┐  │
│        │ │ Search & Filter Bar (White 3D Card)  │  │
│        │ │ [Search] [Filter] [Filter] [Button]  │  │
│        │ └──────────────────────────────────────┘  │
│        │                                            │
│        │ ┌──────────────────────────────────────┐  │
│        │ │ Users Table (Gradient Header)        │  │
│        │ │ Rows hover with peach background     │  │
│        │ │ [View] [Edit] [Delete] buttons       │  │
│        │ └──────────────────────────────────────┘  │
└────────┴────────────────────────────────────────────┘
```

## 🔧 Quick CSS Snippets

### Add 3D Card Effect to Any Element
```css
.my-element {
    background: var(--peach);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    box-shadow: var(--shadow-3d);
    transition: all 0.3s ease;
}

.my-element:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(232, 180, 188, 0.25);
}
```

### Create Gradient Button
```css
.my-button {
    background: linear-gradient(135deg, var(--dusty-rose), var(--dusty-rose-dark));
    color: white;
    padding: 0.75rem 1.75rem;
    border-radius: 12px;
    border: none;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}

.my-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
```

### Style Input with Pastel Focus
```css
.my-input {
    background: var(--white);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
}

.my-input:focus {
    border-color: var(--dusty-rose);
    box-shadow: 0 0 0 0.2rem rgba(232, 180, 188, 0.25);
    outline: none;
}
```

---

**Pro Tip**: Always use the CSS variables instead of hardcoded colors to maintain consistency and enable easy theme changes!
