# Smart Diet & Lifestyle Planner - Pastel Wellness Theme Update

## 🎨 Design Overview

Your application has been completely redesigned with a beautiful **Pastel Wellness Theme** inspired by modern health and nutrition dashboards. The new design features:

### Color Palette
- **Tea Pink Background**: `#FAF3F0` - Soft, calming base color
- **Peach Cards**: `#FADADD` - Warm, inviting card backgrounds
- **Dusty Rose Accent**: `#E8B4BC` - Primary accent for buttons and highlights
- **Sage Green**: `#C8D8C0` - Secondary accent for balance
- **Text Dark**: `#4A4A4A` - Easy-to-read dark text
- **Text Muted**: `#8A8A8A` - Secondary text
- **Borders**: `#EDE0DD` - Subtle borders

### 3D Card Effects
- **Soft Shadows**: Multi-layered shadows for depth (`4px 4px 12px` with light highlights)
- **Hover Effects**: Cards lift on hover with enhanced shadows
- **Rounded Corners**: 20px radius for cards, 12px for buttons
- **Gradient Backgrounds**: Smooth gradients for headers and accents

## ✨ New Features

### 1. **Redesigned Login Page**
- Beautiful centered card design with gradient header
- Animated fade-in effect
- Clear demo credentials display
- Registration link prominently displayed
- Heart pulse icon for health theme

### 2. **Admin Dashboard - Full CRUD Operations**

#### User Management Features:
- ✅ **Create**: Add new users with complete form validation
- ✅ **Read**: View all users in a searchable table
- ✅ **Update**: Edit user information (all fields except username)
- ✅ **Delete**: Remove users with confirmation modal
- ✅ **View Details**: Comprehensive user profile view with:
  - Personal information
  - Health metrics (BMI calculation)
  - Goals overview
  - Recent activity logs

#### Search & Filter Bar:
- **Search by Name**: Filter users by first name, last name, or username
- **Filter by Gender**: Male, Female, Other, or All
- **Filter by Role**: Admins Only, Users Only, or All Users
- **Real-time Filtering**: Instant results as you apply filters

#### User Table:
- Beautiful gradient header (Dusty Rose → Sage)
- Hover effects on rows
- Badge indicators for roles and gender
- Action buttons:
  - 👁️ View (Blue)
  - ✏️ Edit (Warning)
  - 🗑️ Delete (Red with confirmation modal)

### 3. **Enhanced Navigation**
- Gradient navbar (Dusty Rose → Sage)
- Smooth sidebar with pastel background gradient
- Active link highlighting
- Hover animations (slides right with color change)
- Icon-based navigation

### 4. **Updated CSS Framework**
- **Pastel Color Variables**: All colors defined in CSS variables
- **3D Shadow System**: Consistent shadow hierarchy (sm, md, lg, 3d)
- **Responsive Design**: Mobile-friendly breakpoints
- **Custom Scrollbar**: Themed scrollbar matching the color scheme
- **Smooth Animations**: Fade-in, transform, and hover effects

## 📂 Files Modified

### 1. `flask_app/static/style.css`
- Complete rewrite with pastel theme
- Added 3D shadow variables
- Gradient backgrounds
- Enhanced button styles
- Table styling with gradients
- Form control enhancements
- Modal and badge styling
- **Backup**: `style_old.css` (original preserved)

### 2. `flask_app/templates/login.html`
- New centered card layout
- Gradient header with heart icon
- Demo credentials section with styled boxes
- Registration link
- Fade-in animation
- **Backup**: `login_old.html` (original preserved)

### 3. `flask_app/templates/admin_dashboard.html`
- Complete restructure
- User CRUD interface
- Search and filter bar
- View user details page
- Create user form
- Update user form
- Delete confirmation modals
- **Backup**: `admin_dashboard_old.html` (original preserved)

### 4. `flask_app/app.py`
- Added 5 new routes for user CRUD:
  - `admin_view_user(user_id)` - View detailed user info
  - `admin_create_user()` - Create new user (GET/POST)
  - `admin_update_user(user_id)` - Update user (GET/POST)
  - `admin_delete_user(user_id)` - Delete user (POST)
  - Updated `admin_users()` - Added search and filter support

## 🚀 How to Use

### Access the Application
**URL**: http://127.0.0.1:5001

### Login Credentials
**Admin Account**:
- Username: `zainab_moazzam`
- Password: `hashed_password_123`

**User Account**:
- Username: `test_user1`
- Password: `hashed_password_test1`

### Admin User Management Workflow

#### 1. View All Users
- Navigate to "Manage Users" in sidebar
- See all users in a beautiful table with 3D cards
- Observe role badges (Admin/User) and gender badges

#### 2. Search Users
- Use the search bar to find users by name or username
- Type partial names for instant filtering
- Clear search to see all users again

#### 3. Filter Users
- **By Gender**: Select Male, Female, Other, or All
- **By Role**: Select Admin, User, or All
- Click "Filter" button to apply
- Filters work in combination with search

#### 4. View User Details
- Click the 👁️ (eye) icon next to any user
- See comprehensive user profile with:
  - Personal information card with avatar
  - Health metrics (Weight, Height, BMI, Activity Level)
  - Goals tracking
  - Recent daily logs table
- Click "Back to Users" to return

#### 5. Create New User
- Click "Add New User" button at top
- Fill out the comprehensive form:
  - **Required**: Username, Email, Password, First Name, Last Name
  - **Optional**: DOB, Gender, Weight, Height, Activity Level
  - **Admin Role**: Check box to grant admin privileges
- Click "Create User" to save
- User appears immediately in the table

#### 6. Update User
- Click the ✏️ (pencil) icon next to any user
- Modify any field except username
- Update:
  - Email, Name, DOB
  - Health metrics (Weight, Height)
  - Activity level
  - Admin role checkbox
- Click "Update User" to save changes

#### 7. Delete User
- Click the 🗑️ (trash) icon next to any user
- Beautiful modal appears asking for confirmation
- Shows username to confirm deletion
- Click "Delete User" to permanently remove
- **Note**: You cannot delete your own account

## 🎯 Design Highlights

### Wellness Aesthetic
- **Calming Colors**: Pastel palette reduces visual strain
- **Soft Shadows**: 3D effects without harsh contrasts
- **Rounded Corners**: Everything is smoothly rounded (12-24px)
- **Minimal Contrast**: Easy on the eyes for extended use
- **Health Icons**: Heart pulse, activity tracker icons throughout

### User Experience
- **Instant Feedback**: Alerts for all actions (success/error)
- **Confirmation Dialogs**: Prevent accidental deletions
- **Hover States**: Visual feedback on all interactive elements
- **Responsive Layout**: Works on desktop and mobile
- **Fast Search**: Client-side filtering for instant results
- **Loading States**: Smooth transitions and animations

### Accessibility
- **High Contrast Text**: Dark text on light backgrounds
- **Icon + Text Labels**: Visual and text indicators
- **Form Validation**: Required field indicators
- **Error Messages**: Clear, actionable error feedback
- **Keyboard Navigation**: Tab through all controls

## 📊 Database Integration

All CRUD operations are fully integrated with your Oracle database:

### Create User
```sql
INSERT INTO USERS (username, email, password_hash, first_name, last_name,
    date_of_birth, gender, weight, height, activity_level, is_admin)
VALUES (...)
```

### Read Users (with filters)
```sql
SELECT user_id, username, email, first_name, last_name, gender, ...
FROM USERS 
WHERE UPPER(first_name) LIKE UPPER(:search)
  AND gender = :gender
  AND is_admin = :is_admin
ORDER BY user_id DESC
```

### Update User
```sql
UPDATE USERS SET
    email = :email, first_name = :first_name, ...
WHERE user_id = :user_id
```

### Delete User
```sql
DELETE FROM USERS WHERE user_id = :user_id
```

## 🔒 Security Features

- **Admin-Only Access**: All routes check `is_admin` flag
- **Session Management**: User must be logged in
- **Self-Deletion Prevention**: Admin cannot delete their own account
- **Input Validation**: Form validation on both client and server
- **SQL Injection Protection**: Parameterized queries throughout
- **Password Hashing**: (Note: In production, implement proper hashing)

## 🎨 Customization

To customize colors, edit `flask_app/static/style.css`:

```css
:root {
    --tea-pink: #FAF3F0;      /* Background */
    --peach: #FADADD;          /* Cards */
    --dusty-rose: #E8B4BC;     /* Primary accent */
    --sage: #C8D8C0;           /* Secondary accent */
    --text-dark: #4A4A4A;      /* Main text */
    --text-muted: #8A8A8A;     /* Secondary text */
    --border-color: #EDE0DD;   /* Borders */
}
```

## 📱 Responsive Breakpoints

- **Desktop**: Full layout with sidebar (≥992px)
- **Tablet**: Collapsible sidebar (768-991px)
- **Mobile**: Stacked layout, off-canvas sidebar (<768px)

## 🚧 Future Enhancements

Consider adding these features:
- [ ] Bulk user operations (delete multiple)
- [ ] Export user data to CSV/Excel
- [ ] User activity timeline
- [ ] Advanced analytics dashboard
- [ ] Email notifications for new users
- [ ] Password reset functionality
- [ ] Two-factor authentication
- [ ] User roles beyond admin/user
- [ ] Audit log for user changes

## 🐛 Troubleshooting

### Styles Not Loading
- Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
- Clear browser cache
- Check browser console for errors

### CRUD Operations Not Working
- Verify Oracle database connection
- Check session is active (logged in as admin)
- Review Flask terminal output for SQL errors
- Ensure user_id in session matches admin user

### Search/Filter Not Working
- Check URL parameters in browser
- Verify query string formatting
- Review app.py admin_users() route for bugs

## 📞 Support

For issues or questions:
1. Check browser console (F12) for JavaScript errors
2. Review Flask terminal output for Python errors
3. Verify database connection with `test_db_connection.py`
4. Review USER_GUIDE.md for general application help

---

**Congratulations!** Your application now has a beautiful, modern pastel wellness theme with full CRUD operations for user management. The design is professional, user-friendly, and perfectly suited for a health and nutrition application.

Enjoy managing your Smart Diet & Lifestyle Planner! 🌸💚✨
