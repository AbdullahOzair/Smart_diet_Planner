# ================================================================
# SMART DIET ADVISOR - Practical AI Recommendation System
# ================================================================
# User-Friendly AI that analyzes real user data and provides
# actionable suggestions for diet, exercise, and mood
# ================================================================

import psycopg2
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random

class SmartDietAdvisor:
    """
    Practical AI Advisor that analyzes user's actual data from database
    and provides personalized, actionable recommendations
    """
    
    def __init__(self, pg_host='localhost', pg_port='5432', pg_database='smart_diet_planner',
                 pg_user='postgres', pg_password='postgres'):
        import os
        self._pg_params = dict(
            host=os.getenv('PG_HOST', pg_host),
            port=os.getenv('PG_PORT', pg_port),
            database=os.getenv('PG_DATABASE', pg_database),
            user=os.getenv('PG_USER', pg_user),
            password=os.getenv('PG_PASSWORD', pg_password),
        )
        print("🤖 Smart Diet Advisor initialized!")

    @staticmethod
    def _pg(query, params=None):
        """Convert Oracle :name params to psycopg2 %(name)s params."""
        if params and isinstance(params, dict):
            return re.sub(r':([a-zA-Z_]\w*)', r'%(\1)s', query), params
        return query, params

    def get_db_connection(self):
        """Get database connection"""
        try:
            return psycopg2.connect(**self._pg_params)
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def analyze_user_data(self, user_id: int, goal: str) -> Dict:
        """
        Main analysis method that gathers and analyzes all user data
        
        Args:
            user_id: User ID
            goal: User's goal (weight_loss, weight_gain, maintain)
        
        Returns:
            Complete analysis with actionable recommendations
        """
        print(f"\n🔍 Analyzing data for user {user_id}...")
        
        conn = self.get_db_connection()
        if not conn:
            return self._get_fallback_recommendation(goal)
        
        try:
            cursor = conn.cursor()
            
            # Gather all user data
            user_profile = self._get_user_profile(cursor, user_id)
            daily_logs = self._get_daily_logs(cursor, user_id)
            meal_logs = self._get_meal_logs(cursor, user_id)
            activity_logs = self._get_activity_logs(cursor, user_id)
            mood_logs = self._get_mood_logs(cursor, user_id)
            user_goals = self._get_user_goals(cursor, user_id)
            
            # Calculate data quality score
            data_quality = self._calculate_data_quality(daily_logs, meal_logs, activity_logs, mood_logs)
            
            # Analyze patterns
            calorie_analysis = self._analyze_calories(daily_logs, user_profile, goal)
            activity_analysis = self._analyze_activities(activity_logs, goal)
            mood_analysis = self._analyze_mood(mood_logs)
            meal_analysis = self._analyze_meals(meal_logs, goal)
            progress_analysis = self._analyze_progress(daily_logs, user_goals)
            
            # Generate recommendations
            food_recommendations = self._recommend_foods(meal_analysis, calorie_analysis, goal)
            activity_recommendations = self._recommend_activities(activity_analysis, calorie_analysis, goal)
            mood_recommendations = self._recommend_mood_improvements(mood_analysis, activity_logs)
            lifestyle_tips = self._generate_lifestyle_tips(daily_logs, goal)
            
            # Create user-friendly explanation
            explanation = self._create_explanation(
                user_profile, calorie_analysis, activity_analysis,
                mood_analysis, progress_analysis, goal
            )
            
            # Calculate confidence based on data quality
            confidence = self._calculate_confidence(data_quality, daily_logs)
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'recommendation': calorie_analysis['primary_advice'],
                'explanation': explanation,
                'ai_confidence': confidence,
                'food_recommendations': food_recommendations,
                'activity_recommendations': activity_recommendations,
                'mood_recommendations': mood_recommendations,
                'lifestyle_tips': lifestyle_tips,
                'data_quality': data_quality,
                'progress_summary': progress_analysis
            }
            
        except Exception as e:
            print(f"❌ Error analyzing user data: {e}")
            if conn:
                conn.close()
            return self._get_fallback_recommendation(goal)
    
    def _get_user_profile(self, cursor, user_id: int) -> Dict:
        """Get user profile information"""
        cursor.execute(*self._pg("""
            SELECT weight, height, 
                   EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM date_of_birth) as age,
                   activity_level, gender, first_name
            FROM USERS WHERE user_id = :user_id
        """, {'user_id': user_id}))
        
        result = cursor.fetchone()
        if result:
            weight, height, age, activity_level, gender, first_name = result
            height_m = height / 100
            bmi = weight / (height_m ** 2) if height_m > 0 else 25
            
            return {
                'weight': weight,
                'height': height,
                'age': age,
                'activity_level': activity_level,
                'gender': gender,
                'first_name': first_name,
                'bmi': round(bmi, 1)
            }
        return {'weight': 70, 'height': 170, 'age': 25, 'bmi': 24, 'first_name': 'User'}
    
    def _get_daily_logs(self, cursor, user_id: int) -> List[Dict]:
        """Get last 30 days of daily logs"""
        cursor.execute(*self._pg("""
            SELECT total_calories_consumed, total_calories_burned, 
                   water_intake, sleep_hours, weight, notes,
                   TO_CHAR(log_date, 'YYYY-MM-DD') as log_date
            FROM DAILY_LOG 
            WHERE user_id = :user_id 
            AND log_date >= CURRENT_DATE - 30
            ORDER BY log_date DESC
        """, {'user_id': user_id}))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                'calories_consumed': row[0] or 0,
                'calories_burned': row[1] or 0,
                'water_intake': row[2] or 0,
                'sleep_hours': row[3] or 0,
                'weight': row[4] or 0,
                'notes': row[5] or '',
                'date': row[6]
            })
        return logs
    
    def _get_meal_logs(self, cursor, user_id: int) -> List[Dict]:
        """Get recent meal logs with details"""
        cursor.execute(*self._pg("""
            SELECT m.meal_name, m.meal_category, m.calories, m.protein,
                   ml.quantity, ml.total_calories,
                   TO_CHAR(ml.meal_time, 'YYYY-MM-DD HH24:MI') as meal_time
            FROM MEAL_LOG ml
            JOIN MEALS m ON ml.meal_id = m.meal_id
            JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
            WHERE d.user_id = :user_id
            AND d.log_date >= CURRENT_DATE - 14
            ORDER BY ml.meal_time DESC
        """, {'user_id': user_id}))
        
        meals = []
        for row in cursor.fetchall():
            meals.append({
                'name': row[0],
                'category': row[1],
                'calories': row[2],
                'protein': row[3],
                'quantity': row[4],
                'total_calories': row[5],
                'time': row[6]
            })
        return meals
    
    def _get_activity_logs(self, cursor, user_id: int) -> List[Dict]:
        """Get recent activity logs"""
        cursor.execute(*self._pg("""
            SELECT a.activity_name, a.activity_category, a.intensity_level,
                   al.duration_minutes, al.calories_burned,
                   TO_CHAR(al.activity_time, 'YYYY-MM-DD') as activity_date
            FROM ACTIVITY_LOG al
            JOIN ACTIVITIES a ON al.activity_id = a.activity_id
            JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
            WHERE d.user_id = :user_id
            AND d.log_date >= CURRENT_DATE - 14
            ORDER BY al.activity_time DESC
        """, {'user_id': user_id}))
        
        activities = []
        for row in cursor.fetchall():
            activities.append({
                'name': row[0],
                'category': row[1],
                'intensity': row[2],
                'duration': row[3],
                'calories_burned': row[4],
                'date': row[5]
            })
        return activities
    
    def _get_mood_logs(self, cursor, user_id: int) -> List[Dict]:
        """Get recent mood logs"""
        cursor.execute(*self._pg("""
            SELECT ml.mood_rating, ml.stress_level, ml.energy_level, ml.notes,
                   TO_CHAR(d.log_date, 'YYYY-MM-DD') as log_date
            FROM MOOD_LOG ml
            JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
            WHERE d.user_id = :user_id
            AND d.log_date >= CURRENT_DATE - 14
            ORDER BY d.log_date DESC
        """, {'user_id': user_id}))
        
        moods = []
        for row in cursor.fetchall():
            moods.append({
                'mood_rating': row[0],
                'stress_level': row[1],
                'energy_level': row[2],
                'notes': row[3] or '',
                'date': row[4]
            })
        return moods
    
    def _get_user_goals(self, cursor, user_id: int) -> List[Dict]:
        """Get user's active goals"""
        cursor.execute("""
            SELECT goal_type, target_value, current_value, 
                   TO_CHAR(start_date, 'YYYY-MM-DD') as start_date,
                   TO_CHAR(target_date, 'YYYY-MM-DD') as target_date
            FROM GOALS 
            WHERE user_id = :user_id AND status = 'Active'
        """, {'user_id': user_id})
        
        goals = []
        for row in cursor.fetchall():
            goals.append({
                'type': row[0],
                'target': row[1],
                'current': row[2],
                'start_date': row[3],
                'target_date': row[4]
            })
        return goals
    
    def _calculate_data_quality(self, daily_logs, meal_logs, activity_logs, mood_logs) -> Dict:
        """Calculate data quality score"""
        scores = {
            'daily_logs': min(len(daily_logs) / 14 * 100, 100),  # 14 days ideal
            'meal_logs': min(len(meal_logs) / 28 * 100, 100),  # 2 meals/day for 14 days
            'activity_logs': min(len(activity_logs) / 10 * 100, 100),  # 10 activities ideal
            'mood_logs': min(len(mood_logs) / 14 * 100, 100)  # 14 days ideal
        }
        
        overall = sum(scores.values()) / 4
        
        return {
            'overall': round(overall, 1),
            'daily_logs_count': len(daily_logs),
            'meal_logs_count': len(meal_logs),
            'activity_logs_count': len(activity_logs),
            'mood_logs_count': len(mood_logs)
        }
    
    def _analyze_calories(self, daily_logs: List[Dict], user_profile: Dict, goal: str) -> Dict:
        """Analyze calorie patterns and provide advice"""
        if not daily_logs:
            return {
                'avg_consumed': 0,
                'avg_burned': 0,
                'net_balance': 0,
                'primary_advice': 'Start logging your meals to get personalized calorie advice'
            }
        
        total_consumed = sum(log['calories_consumed'] for log in daily_logs)
        total_burned = sum(log['calories_burned'] for log in daily_logs)
        avg_consumed = total_consumed / len(daily_logs)
        avg_burned = total_burned / len(daily_logs)
        net_balance = avg_consumed - avg_burned
        
        # Calculate recommended calories based on BMI and goal
        bmi = user_profile['bmi']
        if goal == 'weight_loss':
            if net_balance > 300:
                advice = f"You're averaging {int(avg_consumed)} calories/day. To lose weight, reduce intake by 400-500 calories."
            elif net_balance > 0:
                advice = f"Good progress! Keep your calorie deficit consistent to continue losing weight."
            else:
                advice = f"You're burning more than consuming. Add 200-300 healthy calories to avoid muscle loss."
        elif goal == 'weight_gain':
            if net_balance < 200:
                advice = f"Increase your daily intake by 400-500 calories with protein-rich foods to gain weight."
            else:
                advice = f"Great! Your calorie surplus of {int(net_balance)} calories/day supports healthy weight gain."
        else:  # maintain
            if abs(net_balance) < 200:
                advice = f"Perfect balance! Your current intake of {int(avg_consumed)} calories/day maintains your weight."
            elif net_balance > 200:
                advice = f"You're eating {int(net_balance)} more calories than you burn. Reduce portions slightly."
            else:
                advice = f"You're in a deficit. Add {abs(int(net_balance))} calories to maintain your weight."
        
        return {
            'avg_consumed': round(avg_consumed, 0),
            'avg_burned': round(avg_burned, 0),
            'net_balance': round(net_balance, 0),
            'primary_advice': advice,
            'days_analyzed': len(daily_logs)
        }
    
    def _analyze_activities(self, activity_logs: List[Dict], goal: str) -> Dict:
        """Analyze activity patterns"""
        if not activity_logs:
            return {
                'total_activities': 0,
                'avg_duration': 0,
                'total_calories_burned': 0,
                'most_common_activity': 'None',
                'needs_more': True
            }
        
        total_duration = sum(a['duration'] for a in activity_logs)
        total_calories = sum(a['calories_burned'] for a in activity_logs)
        avg_duration = total_duration / len(activity_logs)
        
        # Find most common activity category
        categories = {}
        for activity in activity_logs:
            cat = activity['category']
            categories[cat] = categories.get(cat, 0) + 1
        most_common = max(categories.items(), key=lambda x: x[1])[0] if categories else 'None'
        
        needs_more = len(activity_logs) < 7  # Less than 7 activities in 2 weeks
        
        return {
            'total_activities': len(activity_logs),
            'avg_duration': round(avg_duration, 1),
            'total_calories_burned': round(total_calories, 0),
            'most_common_activity': most_common,
            'needs_more': needs_more,
            'activity_categories': categories
        }
    
    def _analyze_mood(self, mood_logs: List[Dict]) -> Dict:
        """Analyze mood patterns"""
        if not mood_logs:
            return {
                'avg_mood': 0,
                'avg_stress': 0,
                'avg_energy': 0,
                'mood_trend': 'Unknown',
                'needs_attention': False
            }
        
        total_mood = sum(m['mood_rating'] for m in mood_logs)
        avg_mood = total_mood / len(mood_logs)
        
        # Count stress levels
        stress_counts = {'Low': 0, 'Moderate': 0, 'High': 0}
        energy_counts = {'Low': 0, 'Moderate': 0, 'High': 0}
        
        for mood in mood_logs:
            stress_counts[mood['stress_level']] = stress_counts.get(mood['stress_level'], 0) + 1
            energy_counts[mood['energy_level']] = energy_counts.get(mood['energy_level'], 0) + 1
        
        high_stress = stress_counts.get('High', 0) > len(mood_logs) * 0.4
        low_energy = energy_counts.get('Low', 0) > len(mood_logs) * 0.4
        needs_attention = avg_mood < 3 or high_stress or low_energy
        
        if avg_mood >= 4:
            trend = 'Great'
        elif avg_mood >= 3:
            trend = 'Good'
        else:
            trend = 'Needs Improvement'
        
        return {
            'avg_mood': round(avg_mood, 1),
            'stress_distribution': stress_counts,
            'energy_distribution': energy_counts,
            'mood_trend': trend,
            'needs_attention': needs_attention,
            'high_stress': high_stress,
            'low_energy': low_energy
        }
    
    def _analyze_meals(self, meal_logs: List[Dict], goal: str) -> Dict:
        """Analyze meal patterns"""
        if not meal_logs:
            return {
                'total_meals': 0,
                'avg_calories_per_meal': 0,
                'most_common_category': 'Unknown',
                'protein_intake': 'Unknown'
            }
        
        total_calories = sum(m['total_calories'] for m in meal_logs)
        total_protein = sum(m['protein'] * m['quantity'] for m in meal_logs)
        avg_calories = total_calories / len(meal_logs)
        
        # Category distribution
        categories = {}
        for meal in meal_logs:
            cat = meal['category']
            categories[cat] = categories.get(cat, 0) + 1
        most_common = max(categories.items(), key=lambda x: x[1])[0] if categories else 'Unknown'
        
        return {
            'total_meals': len(meal_logs),
            'avg_calories_per_meal': round(avg_calories, 0),
            'total_protein': round(total_protein, 1),
            'most_common_category': most_common,
            'category_distribution': categories
        }
    
    def _analyze_progress(self, daily_logs: List[Dict], user_goals: List[Dict]) -> Dict:
        """Analyze progress towards goals"""
        if not daily_logs or len(daily_logs) < 3:
            return {
                'weight_change': 0,
                'progress_status': 'Need more data',
                'days_tracked': len(daily_logs)
            }
        
        # Get weight change
        recent_weights = [log['weight'] for log in daily_logs if log['weight'] > 0]
        if len(recent_weights) >= 2:
            weight_change = recent_weights[0] - recent_weights[-1]
            
            if abs(weight_change) < 0.5:
                status = 'Stable weight'
            elif weight_change > 0:
                status = f'Gained {abs(weight_change):.1f} kg'
            else:
                status = f'Lost {abs(weight_change):.1f} kg'
        else:
            weight_change = 0
            status = 'Insufficient weight data'
        
        return {
            'weight_change': round(weight_change, 1),
            'progress_status': status,
            'days_tracked': len(daily_logs),
            'consistent_logging': len(daily_logs) >= 14
        }
    
    def _recommend_foods(self, meal_analysis: Dict, calorie_analysis: Dict, goal: str) -> List[str]:
        """Recommend specific foods based on goal"""
        recommendations = []
        
        if goal == 'weight_loss':
            recommendations.extend([
                "🥗 Grilled Chicken Salad - High protein, low calories (250 cal)",
                "🐟 Baked Salmon with Steamed Vegetables - Omega-3 rich (350 cal)",
                "🥚 Egg White Omelette with Spinach - Filling breakfast (180 cal)",
                "🍎 Greek Yogurt with Berries - Perfect snack (150 cal)",
                "🥦 Vegetable Stir-Fry with Tofu - Nutrient-dense dinner (280 cal)"
            ])
        elif goal == 'weight_gain':
            recommendations.extend([
                "🥜 Peanut Butter Banana Smoothie - Calorie-rich breakfast (450 cal)",
                "🍝 Whole Grain Pasta with Chicken - High carbs & protein (550 cal)",
                "🥑 Avocado Toast with Eggs - Healthy fats (400 cal)",
                "🥩 Beef Steak with Sweet Potato - Muscle building (600 cal)",
                "🌰 Trail Mix with Dried Fruits - Energy-dense snack (350 cal)"
            ])
        else:  # maintain
            recommendations.extend([
                "🍲 Balanced Buddha Bowl - Veggies, quinoa, chicken (400 cal)",
                "🐠 Grilled Fish with Brown Rice - Complete meal (420 cal)",
                "🥙 Turkey Wrap with Hummus - Balanced lunch (380 cal)",
                "🍳 Scrambled Eggs with Toast - Good breakfast (320 cal)",
                "🥤 Protein Smoothie with Oats - Post-workout (300 cal)"
            ])
        
        return recommendations[:5]
    
    def _recommend_activities(self, activity_analysis: Dict, calorie_analysis: Dict, goal: str) -> List[str]:
        """Recommend specific activities based on goal and current patterns"""
        recommendations = []
        
        if goal == 'weight_loss':
            recommendations.extend([
                "🏃‍♂️ Running - 30-45 minutes (burns 300-500 calories)",
                "🚴‍♀️ Cycling - 45 minutes (burns 400-600 calories)",
                "💪 HIIT Workout - 20 minutes (burns 250-400 calories)",
                "🏊‍♂️ Swimming - 30 minutes (burns 350-500 calories)",
                "⛰️ Hiking - 1 hour (burns 400-550 calories)"
            ])
        elif goal == 'weight_gain':
            recommendations.extend([
                "🏋️‍♂️ Weight Lifting - 45 minutes (build muscle mass)",
                "💪 Strength Training - 30 minutes (muscle growth)",
                "🦵 Squats & Deadlifts - 3 sets of 10 (leg muscle building)",
                "🤸‍♂️ Resistance Band Exercises - 30 minutes (muscle toning)",
                "🏋️ Compound Movements - Focus on major muscle groups"
            ])
        else:  # maintain
            recommendations.extend([
                "🚶‍♂️ Brisk Walking - 45 minutes daily (maintain fitness)",
                "🧘‍♀️ Yoga - 30 minutes (flexibility & balance)",
                "🏃‍♀️ Light Jogging - 20-30 minutes (cardio health)",
                "🚴 Casual Cycling - 30 minutes (enjoyable cardio)",
                "⚽ Sports Activities - Basketball, soccer (fun exercise)"
            ])
        
        # Add specific recommendations based on activity gaps
        if activity_analysis['needs_more']:
            recommendations.insert(0, "⚠️ You need more physical activity! Aim for at least 3-4 workouts per week.")
        
        return recommendations[:5]
    
    def _recommend_mood_improvements(self, mood_analysis: Dict, activity_logs: List[Dict]) -> List[str]:
        """Recommend mood improvement strategies"""
        recommendations = []
        
        if mood_analysis['needs_attention']:
            recommendations.append("😊 MOOD IMPROVEMENT TIPS:")
            
            if mood_analysis['high_stress']:
                recommendations.extend([
                    "🧘 Practice meditation or deep breathing - 10 minutes daily",
                    "🚶 Take short walks outdoors - sunlight improves mood",
                    "📝 Journal your thoughts - reduces stress and anxiety"
                ])
            
            if mood_analysis['low_energy']:
                recommendations.extend([
                    "😴 Prioritize 7-8 hours of quality sleep",
                    "💧 Stay hydrated - drink 8-10 glasses of water daily",
                    "🍎 Eat energy-boosting foods - nuts, fruits, whole grains"
                ])
            
            if mood_analysis['avg_mood'] < 3:
                recommendations.extend([
                    "👥 Connect with friends or family - social support matters",
                    "🎵 Listen to uplifting music - proven mood booster",
                    "🏃 Exercise releases endorphins - nature's mood elevator"
                ])
        else:
            recommendations.extend([
                "✅ Your mood is good! Keep maintaining your current lifestyle",
                "😊 Continue your positive habits - exercise, sleep, nutrition",
                "🎯 Set small daily goals to stay motivated and happy"
            ])
        
        return recommendations[:5]
    
    def _generate_lifestyle_tips(self, daily_logs: List[Dict], goal: str) -> List[str]:
        """Generate general lifestyle tips"""
        tips = []
        
        if daily_logs:
            avg_water = sum(log['water_intake'] for log in daily_logs if log['water_intake'] > 0) / len(daily_logs) if daily_logs else 0
            avg_sleep = sum(log['sleep_hours'] for log in daily_logs if log['sleep_hours'] > 0) / len(daily_logs) if daily_logs else 0
            
            if avg_water < 6:
                tips.append("💧 Increase water intake to 8-10 glasses per day")
            if avg_sleep < 7:
                tips.append("😴 Aim for 7-8 hours of sleep for better recovery")
        
        tips.extend([
            "🍽️ Eat smaller, frequent meals to maintain steady energy",
            "📱 Reduce screen time before bed for better sleep quality",
            "🥗 Fill half your plate with vegetables at each meal",
            "⏰ Maintain consistent meal and sleep times"
        ])
        
        return tips[:4]
    
    def _calculate_confidence(self, data_quality: Dict, daily_logs: List[Dict]) -> float:
        """Calculate confidence score based on data quality"""
        # Base confidence on data quality
        base_confidence = data_quality['overall'] / 100
        
        # Boost for consistency
        if data_quality['daily_logs_count'] >= 10:
            base_confidence += 0.15
        if data_quality['meal_logs_count'] >= 20:
            base_confidence += 0.10
        if data_quality['activity_logs_count'] >= 5:
            base_confidence += 0.10
        
        # Cap at 95%
        return min(0.95, max(0.60, base_confidence))
    
    def _create_explanation(self, user_profile: Dict, calorie_analysis: Dict,
                          activity_analysis: Dict, mood_analysis: Dict,
                          progress_analysis: Dict, goal: str) -> str:
        """Create user-friendly explanation"""
        
        name = user_profile['first_name']
        
        explanation_parts = [
            f"👋 Hi {name}! Here's your personalized diet and fitness analysis:",
            "",
            "📊 YOUR CURRENT STATUS:",
            f"• BMI: {user_profile['bmi']} ({'Normal' if 18.5 <= user_profile['bmi'] < 25 else 'Attention needed'})",
            f"• Daily Calories: {int(calorie_analysis['avg_consumed'])} consumed, {int(calorie_analysis['avg_burned'])} burned",
            f"• Net Balance: {int(calorie_analysis['net_balance'])} calories/day",
            f"• Progress: {progress_analysis['progress_status']}",
            "",
            "🎯 YOUR GOAL:",
            f"• {goal.replace('_', ' ').title()}",
            "",
            "💡 CALORIE GUIDANCE:",
            f"• {calorie_analysis['primary_advice']}",
            ""
        ]
        
        if activity_analysis['total_activities'] > 0:
            explanation_parts.extend([
                "🏃 ACTIVITY ANALYSIS:",
                f"• You've done {activity_analysis['total_activities']} activities (avg {activity_analysis['avg_duration']} min each)",
                f"• Total calories burned from exercise: {int(activity_analysis['total_calories_burned'])}",
                f"• Most common: {activity_analysis['most_common_activity']}",
                ""
            ])
        else:
            explanation_parts.extend([
                "🏃 ACTIVITY ANALYSIS:",
                "• ⚠️ No activities logged yet. Start exercising to reach your goal faster!",
                ""
            ])
        
        if mood_analysis['avg_mood'] > 0:
            explanation_parts.extend([
                "😊 MOOD & WELLNESS:",
                f"• Average mood: {mood_analysis['avg_mood']}/5 ({mood_analysis['mood_trend']})",
                f"• Stress levels: {'High stress detected - check recommendations' if mood_analysis['high_stress'] else 'Manageable'}",
                f"• Energy levels: {'Low energy - improve sleep/nutrition' if mood_analysis['low_energy'] else 'Good'}",
                ""
            ])
        
        explanation_parts.extend([
            "📈 WHAT TO DO NEXT:",
            "1. Follow the food recommendations below",
            "2. Do the suggested activities 3-4 times per week",
            "3. Track your daily progress consistently",
            "4. Check back weekly for updated recommendations",
            "",
            "💪 You've got this! Consistency is the key to success!"
        ])
        
        return "\n".join(explanation_parts)
    
    def _get_fallback_recommendation(self, goal: str) -> Dict:
        """Fallback recommendation when data is insufficient"""
        fallback_advice = {
            'weight_loss': "Start by reducing your daily calorie intake by 500 calories. Focus on lean proteins, vegetables, and whole grains. Exercise 30-45 minutes, 4-5 times per week.",
            'weight_gain': "Increase your daily calorie intake by 400-500 calories with protein-rich foods and healthy fats. Focus on strength training 3-4 times per week.",
            'maintain': "Maintain a balanced diet with equal amounts of proteins, carbs, and fats. Exercise 30 minutes daily and stay hydrated."
        }
        
        return {
            'success': True,
            'recommendation': fallback_advice.get(goal, "Consult a nutritionist for personalized advice"),
            'explanation': "⚠️ Limited data available. Start logging your meals, activities, and mood daily for better personalized recommendations!",
            'ai_confidence': 0.65,
            'food_recommendations': self._recommend_foods({}, {}, goal),
            'activity_recommendations': self._recommend_activities({'needs_more': True}, {}, goal),
            'mood_recommendations': ["😊 Start your day with positivity", "🏃 Exercise regularly to boost mood"],
            'lifestyle_tips': ["📝 Log your daily meals and activities", "💧 Drink 8 glasses of water daily"],
            'data_quality': {'overall': 20}
        }


# ================================================================
# MAIN FUNCTION FOR FLASK INTEGRATION
# ================================================================
advisor = SmartDietAdvisor()

def get_smart_recommendation(user_id: int, goal: str) -> Dict:
    """
    Main function for Flask integration
    
    Usage:
    from smart_advisor import get_smart_recommendation
    result = get_smart_recommendation(user_id=1, goal='weight_loss')
    """
    return advisor.analyze_user_data(user_id, goal)


if __name__ == "__main__":
    # Test the advisor
    print("🧪 Testing Smart Diet Advisor...")
    result = get_smart_recommendation(user_id=1, goal='weight_loss')
    print("\n" + "="*60)
    print("TEST RESULTS:")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"AI Confidence: {result['ai_confidence']:.1%}")
    print("\nExplanation:")
    print(result['explanation'])
    print("\nFood Recommendations:")
    for food in result['food_recommendations']:
        print(f"  {food}")
    print("="*60)
