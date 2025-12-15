# Smart Diet & Lifestyle Planner

## Project Overview
The Smart Diet & Lifestyle Planner is an intelligent application that helps users manage their diet, track physical activities, and achieve health goals using AI-powered recommendations.

## Features
- **User Management**: Secure registration and authentication
- **Diet Logging**: Track daily meals and nutritional intake
- **Activity Tracking**: Log physical activities and calories burned
- **AI Recommendations**: Personalized meal plans and lifestyle suggestions
- **Progress Reports**: Visual analytics and progress tracking
- **Goal Setting**: Set and monitor health and fitness goals

## Technology Stack
- **Frontend**: Python Tkinter (GUI)
- **Backend**: Python (Business Logic)
- **Database**: Oracle SQL
- **AI Components**: 
  - Fuzzy Logic for health assessments
  - Rule-based reasoning for recommendations
  - Search algorithms for meal optimization
  - Text generation for personalized advice

## Project Structure
```
SmartDietPlanner/
├── presentation/       # UI Layer (Tkinter)
├── business/          # Business Logic & AI
├── data_access/       # Database Access Layer (DAOs)
├── database/          # SQL Scripts
├── utils/             # Utilities and Helpers
├── main.py            # Application Entry Point
└── requirements.txt   # Python Dependencies
```

## Architecture
This project follows a **3-Tier Architecture**:

### 1. Presentation Layer (UI)
- User interface using Tkinter
- Forms for login, registration, logging, and reports
- Visualization of data using matplotlib

### 2. Business Logic Layer (AI)
- AI agent for intelligent decision making
- Fuzzy logic system for imprecise data handling
- Rule-based reasoning engine
- Search algorithms for optimization
- Diet planning core logic
- Text generation for recommendations

### 3. Data Access Layer
- Database connection management
- Data Access Objects (DAOs) for each entity
- Oracle SQL database interaction

## Installation

### Prerequisites
- Python 3.8 or higher
- Oracle Database 19c or higher
- Oracle Instant Client

### Setup Steps

1. **Clone the repository**
```bash
cd SmartDietPlanner
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Database**
- Edit `utils/constants.py` and update database credentials
- Run SQL scripts in the following order:
  ```bash
  sqlplus username/password@database
  @database/create_tables.sql
  @database/insert_sample_data.sql
  @database/procedures.sql
  @database/functions.sql
  @database/triggers.sql
  @database/indexes.sql
  @database/roles_security.sql
  ```

4. **Run the application**
```bash
python main.py
```

## Database Schema

### Main Tables
- **users**: User account information
- **user_profiles**: Health profiles and physical attributes
- **user_goals**: Health and fitness goals
- **food_database**: Master food nutritional database
- **diet_logs**: Daily food intake logs
- **activity_logs**: Physical activity records
- **meal_plans**: AI-generated meal plans
- **suggestions**: AI recommendations
- **weight_tracking**: Weight history over time

## AI Components

### Fuzzy Logic System
- BMI classification
- Activity level assessment
- Health status evaluation

### Reasoning Engine
- Forward and backward chaining
- Rule-based inference
- Dietary constraint checking

### Search Algorithms
- Meal combination optimization
- A* search for optimal planning
- Hill climbing for local optimization

### Diet Planner
- BMR and TDEE calculations
- Macronutrient distribution
- Personalized meal suggestions

## Usage

### For Users
1. Register an account
2. Complete your health profile
3. Set your health goals
4. Log daily meals and activities
5. View AI-generated recommendations
6. Track progress with reports

### For Developers
- Each layer is independent and modular
- Easy to extend with new features
- Well-documented code with comments
- Follows clean code principles

## Contributing
This is an academic project. For contributions:
1. Follow the existing code structure
2. Add comments for all functions
3. Update documentation
4. Test thoroughly before committing

## Security
- Passwords are hashed using bcrypt
- Row-level security policies implemented
- Database roles and privileges configured
- Input validation and sanitization

## Future Enhancements
- Mobile application integration
- Integration with fitness trackers
- Social features and community support
- Advanced ML models for better predictions
- Recipe recommendations
- Meal preparation planning

## License
Academic Project - [Your University Name]

## Authors
- [Your Name]
- [Team Member Names]

## Acknowledgments
- [Your Professor/Supervisor]
- [Any References or Resources Used]

## Contact
For questions or support:
- Email: [your-email@example.com]
- GitHub: [your-github-username]

---
**Note**: This is a semester project developed for educational purposes.
