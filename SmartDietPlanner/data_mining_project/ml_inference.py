"""
ML Inference Module for Personalized Diet Recommendation System

This module provides a clean interface for loading trained ML models
and making predictions on new nutritional data.

Includes PostgreSQL Database integration for:
- Fetching user goals and daily nutritional logs
- Saving ML predictions to SUGGESTIONS table
- End-to-end recommendation pipeline


"""

import joblib
import numpy as np
try:
    import psycopg2
except ImportError:
    psycopg2 = None
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    """
    Configuration class for PostgreSQL Database connection.
    Store your database credentials here.
    """
    def __init__(self, username: str = None, password: str = None, 
                 dsn: str = None, host: str = "localhost", 
                 port: int = 1521, service_name: str = "XE"):
        """
        Initialize database configuration.
        
        Args:
            username: PostgreSQL DB username
            password: PostgreSQL DB password
            dsn: Full DSN string (optional, overrides host/port/service)
            host: Database host
            port: Database port
            service_name: PostgreSQL service name
        """
        self.username = username or "SYSTEM"
        self.password = password or "your_password"
        
        # If DSN is provided, use it; otherwise construct from components
        if dsn:
            self.dsn = dsn
        else:
            self.dsn = psycopg2.NotUsed(host, port, service_name=service_name)


class PostgreSQLDietRecommendationSystem:
    """
    Extended ML system with PostgreSQL Database integration.
    
    This class handles the complete flow:
    1. Fetch user data from PostgreSQL DB
    2. Transform to ML features
    3. Generate predictions
    4. Save recommendations to DB
    """
    
    def __init__(self, db_config: DatabaseConfig, model_dir: str = "models"):
        """
        Initialize the PostgreSQL-integrated recommendation system.
        
        Args:
            db_config: DatabaseConfig object with connection details
            model_dir: Directory containing ML model files
        """
        self.db_config = db_config
        self.model = DietRecommendationModel(model_dir=model_dir)
        self.connection = None
        
    def connect_to_database(self) -> bool:
        """
        Establish connection to PostgreSQL Database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = psycopg2.connect(
                user=self.db_config.username,
                password=self.db_config.password,
                dsn=self.db_config.dsn
            )
            logger.info("✅ Successfully connected to PostgreSQL Database")
            return True
            
        except psycopg2.DatabaseError as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect_from_database(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def fetch_user_goal(self, user_id: int) -> Optional[int]:
        """
        Fetch user's dietary goal from USERS table.
        
        Flow:
        - Query: SELECT goal FROM USERS WHERE user_id = %(user_id)s
        - Extract goal value (encoded as integer)
        - Return encoded goal or None if not found
        
        Args:
            user_id: User ID to fetch goal for
            
        Returns:
            int: Encoded user goal (e.g., 1=weight_loss, 2=muscle_gain)
        """
        try:
            cursor = self.connection.cursor()
            
            # Query to get user goal
            query = """
                SELECT goal 
                FROM USERS 
                WHERE user_id = %(user_id)s
            """
            
            cursor.execute(query, {"user_id": user_id})
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                user_goal = result[0]
                logger.info(f"✅ User goal fetched: {user_goal} for user_id={user_id}")
                return user_goal
            else:
                logger.warning(f"⚠️ No goal found for user_id={user_id}")
                return None
                
        except psycopg2.DatabaseError as e:
            logger.error(f"❌ Error fetching user goal: {e}")
            return None
    
    def fetch_latest_daily_log(self, user_id: int) -> Optional[Dict[str, float]]:
        """
        Fetch user's latest daily nutritional log from DIET_LOG table.
        
        Flow:
        - Query: Get most recent log entry for user
        - Extract nutritional values: calories, protein, fat, carbs, fiber, sugar, sodium
        - Return as dictionary or None if no data
        
        Args:
            user_id: User ID to fetch log for
            
        Returns:
            Dict with nutritional values or None
        """
        try:
            cursor = self.connection.cursor()
            
            # Query to get latest daily log (most recent date)
            query = """
                SELECT calories, protein, fat, carbs, fiber, sugar, sodium, log_date
                FROM DIET_LOG
                WHERE user_id = %(user_id)s
                ORDER BY log_date DESC
                FETCH FIRST 1 ROWS ONLY
            """
            
            cursor.execute(query, {"user_id": user_id})
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                log_data = {
                    "calories": float(result[0] or 0),
                    "protein": float(result[1] or 0),
                    "fat": float(result[2] or 0),
                    "carbs": float(result[3] or 0),
                    "fiber": float(result[4] or 0),
                    "sugar": float(result[5] or 0),
                    "sodium": float(result[6] or 0),
                    "log_date": result[7]
                }
                logger.info(f"✅ Latest log fetched for user_id={user_id}, date={log_data['log_date']}")
                return log_data
            else:
                logger.warning(f"⚠️ No diet log found for user_id={user_id}")
                return None
                
        except psycopg2.DatabaseError as e:
            logger.error(f"❌ Error fetching daily log: {e}")
            return None
    
    def convert_db_to_ml_features(self, daily_log: Dict[str, float], 
                                user_goal: int) -> Dict[str, float]:
        """
        Convert database values to ML feature vector.
        
        Flow:
        - Take nutritional values from daily log
        - Add user goal (encoded)
        - Format as dictionary matching ML model input
        - Return feature vector ready for prediction
        
        Args:
            daily_log: Dictionary with nutritional data from DB
            user_goal: Encoded user goal from DB
            
        Returns:
            Dict: Feature vector for ML model
        """
        try:
            # Create ML feature vector with exact field names expected by model
            ml_features = {
                "calories": daily_log.get("calories", 0),
                "protein": daily_log.get("protein", 0),
                "fat": daily_log.get("fat", 0),
                "carbs": daily_log.get("carbs", 0),
                "fiber": daily_log.get("fiber", 0),
                "sugar": daily_log.get("sugar", 0),
                "sodium": daily_log.get("sodium", 0),
                "user_goal": user_goal
            }
            
            logger.info(f"✅ ML features prepared: {ml_features}")
            return ml_features
            
        except Exception as e:
            logger.error(f"❌ Error converting DB to ML features: {e}")
            return None
    
    def save_suggestion_to_db(self, user_id: int, prediction_result: Dict[str, Any]) -> bool:
        """
        Save ML prediction to SUGGESTIONS table in PostgreSQL DB.
        
        Flow:
        - Extract prediction details (category, confidence)
        - Generate suggestion_id (sequence or auto-increment)
        - Insert into SUGGESTIONS table
        - Commit transaction
        - Return success status
        
        Args:
            user_id: User ID for the suggestion
            prediction_result: ML prediction result dictionary
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            
            # Extract prediction details
            predicted_category = prediction_result.get("predicted_category", "Unknown")
            confidence = prediction_result.get("confidence_percentage", 0.0)
            
            # Generate suggestion text
            suggestion_text = f"Recommended food category: {predicted_category} (Confidence: {confidence:.2f}%)"
            
            # Insert into SUGGESTIONS table
            # Assuming table structure: (suggestion_id, user_id, suggestion_text, date_created, confidence_score)
            insert_query = """
                INSERT INTO SUGGESTIONS 
                (suggestion_id, user_id, suggestion_text, date_created, confidence_score, category)
                VALUES 
                (suggestion_seq.NEXTVAL, %(user_id)s, %(suggestion_text)s, SYSDATE, %(confidence)s, %(category)s)
            """
            
            cursor.execute(insert_query, {
                "user_id": user_id,
                "suggestion_text": suggestion_text,
                "confidence": confidence,
                "category": predicted_category
            })
            
            # Commit the transaction
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ Suggestion saved to DB for user_id={user_id}: {predicted_category}")
            return True
            
        except psycopg2.DatabaseError as e:
            logger.error(f"❌ Error saving suggestion to DB: {e}")
            # Rollback in case of error
            if self.connection:
                self.connection.rollback()
            return False
    
    def generate_and_save_recommendation(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Complete end-to-end recommendation pipeline.
        
        FLOW:
        1. Connect to PostgreSQL Database
        2. Fetch user goal from USERS table
        3. Fetch latest daily log from DIET_LOG table
        4. Convert DB data to ML feature vector
        5. Load ML models (ANN, scaler, encoder)
        6. Generate prediction using ML model
        7. Save prediction to SUGGESTIONS table
        8. Return complete result
        
        Args:
            user_id: User ID to generate recommendation for
            
        Returns:
            Dict: Complete recommendation result with DB save status
        """
        try:
            logger.info(f"{'='*70}")
            logger.info(f"Starting recommendation pipeline for user_id={user_id}")
            logger.info(f"{'='*70}")
            
            # Step 1: Ensure database connection
            if not self.connection:
                if not self.connect_to_database():
                    return {"status": "error", "message": "Database connection failed"}
            
            # Step 2: Fetch user goal
            user_goal = self.fetch_user_goal(user_id)
            if user_goal is None:
                return {"status": "error", "message": "User goal not found"}
            
            # Step 3: Fetch latest daily log
            daily_log = self.fetch_latest_daily_log(user_id)
            if not daily_log:
                return {"status": "error", "message": "No diet log found for user"}
            
            # Step 4: Convert to ML features
            ml_features = self.convert_db_to_ml_features(daily_log, user_goal)
            if not ml_features:
                return {"status": "error", "message": "Feature conversion failed"}
            
            # Step 5: Load ML models
            if not self.model.is_loaded:
                if not self.model.load_models():
                    return {"status": "error", "message": "ML models failed to load"}
            
            # Step 6: Generate prediction
            prediction_result = self.model.predict(ml_features)
            if not prediction_result or prediction_result["status"] != "success":
                return {"status": "error", "message": "Prediction failed"}
            
            # Step 7: Save to database
            save_success = self.save_suggestion_to_db(user_id, prediction_result)
            
            # Step 8: Return complete result
            complete_result = {
                **prediction_result,
                "user_id": user_id,
                "db_saved": save_success,
                "source_data": daily_log,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info(f"{'='*70}")
            logger.info(f"✅ Recommendation pipeline completed successfully!")
            logger.info(f"{'='*70}")
            
            return complete_result
            
        except Exception as e:
            logger.error(f"❌ Error in recommendation pipeline: {e}")
            return {
                "status": "error",
                "message": str(e),
                "user_id": user_id
            }


# Convenience function for PostgreSQL-integrated recommendations
def get_recommendation_from_db(user_id: int, db_config: DatabaseConfig, 
                               model_dir: str = "models") -> Optional[Dict[str, Any]]:
    """
    Quick function to get recommendation with database integration.
    
    Args:
        user_id: User ID to generate recommendation for
        db_config: Database configuration object
        model_dir: Directory containing ML models
        
    Returns:
        Dict: Recommendation result
    """
    system = PostgreSQLDietRecommendationSystem(db_config, model_dir)
    
    try:
        result = system.generate_and_save_recommendation(user_id)
        return result
    finally:
        system.disconnect_from_database()


class DietRecommendationModel:
    """
    A class to handle ML inference for diet recommendations.
    
    This class loads pre-trained models and provides methods to predict
    food categories based on nutritional information.
    """
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize the DietRecommendationModel.
        
        Args:
            model_dir (str): Directory containing saved model files
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.is_loaded = False
        
    def load_models(self) -> bool:
        """
        Load all required model files (model, scaler, label encoder).
        
        Returns:
            bool: True if all models loaded successfully, False otherwise
        """
        try:
            # Load the trained ANN model
            model_path = self.model_dir / "diet_model.pkl"
            self.model = joblib.load(model_path)
            print(f"✅ Model loaded from {model_path}")
            
            # Load the StandardScaler for feature normalization
            scaler_path = self.model_dir / "scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            print(f"✅ Scaler loaded from {scaler_path}")
            
            # Load the LabelEncoder for category decoding
            encoder_path = self.model_dir / "label_encoder.pkl"
            self.label_encoder = joblib.load(encoder_path)
            print(f"✅ Label Encoder loaded from {encoder_path}")
            
            self.is_loaded = True
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error: Model file not found - {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False
    
    def validate_input(self, user_input: Dict[str, float]) -> bool:
        """
        Validate user input data.
        
        Args:
            user_input (Dict[str, float]): Dictionary containing nutritional values
            
        Returns:
            bool: True if input is valid, False otherwise
        """
        required_fields = [
            'calories', 'protein', 'fat', 'carbs', 
            'fiber', 'sugar', 'sodium', 'user_goal'
        ]
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in user_input:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Validate that all values are numeric
        for field, value in user_input.items():
            if not isinstance(value, (int, float)):
                print(f"❌ Invalid value for {field}: must be numeric")
                return False
        
        return True
    
    def preprocess_input(self, user_input: Dict[str, float]) -> np.ndarray:
        """
        Preprocess user input using the saved scaler.
        
        Args:
            user_input (Dict[str, float]): Raw nutritional data
            
        Returns:
            np.ndarray: Scaled feature array ready for prediction
        """
        # Extract features in the correct order
        # Order must match the training data feature order
        feature_order = [
            'calories', 'protein', 'fat', 'carbs',
            'fiber', 'sugar', 'sodium', 'user_goal'
        ]
        
        # Create feature array
        features = np.array([[user_input[field] for field in feature_order]])
        
        # Apply scaling transformation
        scaled_features = self.scaler.transform(features)
        
        return scaled_features
    
    def predict(self, user_input: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """
        Predict food category based on nutritional input.
        
        Args:
            user_input (Dict[str, float]): Dictionary with nutritional values
            
        Returns:
            Dict[str, Any]: Prediction results in JSON format or None if error
        """
        # Check if models are loaded
        if not self.is_loaded:
            print("❌ Models not loaded. Please call load_models() first.")
            return None
        
        # Validate input
        if not self.validate_input(user_input):
            return None
        
        try:
            # Preprocess the input data
            scaled_features = self.preprocess_input(user_input)
            
            # Make prediction using the ANN model
            prediction_encoded = self.model.predict(scaled_features)
            
            # Get prediction probabilities for confidence scores
            prediction_proba = self.model.predict_proba(scaled_features)
            
            # Decode the prediction to readable category name
            predicted_category = self.label_encoder.inverse_transform(prediction_encoded)[0]
            
            # Get confidence score (probability of predicted class)
            confidence = float(np.max(prediction_proba) * 100)
            
            # Prepare response in JSON format
            response = {
                "status": "success",
                "predicted_category": predicted_category,
                "confidence_percentage": round(confidence, 2),
                "encoded_prediction": int(prediction_encoded[0]),
                "input_data": user_input,
                "message": f"Recommended food category: {predicted_category}"
            }
            
            return response
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return {
                "status": "error",
                "message": str(e),
                "predicted_category": None
            }
    
    def predict_batch(self, user_inputs: list) -> list:
        """
        Predict food categories for multiple inputs (batch prediction).
        
        Args:
            user_inputs (list): List of dictionaries containing nutritional data
            
        Returns:
            list: List of prediction results
        """
        results = []
        for idx, user_input in enumerate(user_inputs):
            print(f"\nProcessing input {idx + 1}/{len(user_inputs)}...")
            result = self.predict(user_input)
            results.append(result)
        
        return results


# Convenience function for single predictions
def get_food_recommendation(user_input: Dict[str, float], 
                           model_dir: str = "models") -> Optional[Dict[str, Any]]:
    """
    Quick function to get a food recommendation without managing the class.
    
    Args:
        user_input (Dict[str, float]): Nutritional data
        model_dir (str): Directory containing model files
        
    Returns:
        Dict[str, Any]: Prediction result
    """
    model = DietRecommendationModel(model_dir=model_dir)
    
    if model.load_models():
        return model.predict(user_input)
    else:
        return {
            "status": "error",
            "message": "Failed to load models",
            "predicted_category": None
        }


# Example usage and testing
if __name__ == "__main__":
    """
    Example usage of the ML inference module.
    This section demonstrates how to use the module for predictions.
    """
    
    print("="*70)
    print("PERSONALIZED DIET RECOMMENDATION SYSTEM - ML INFERENCE MODULE")
    print("="*70)
    
    # Example 1: Using the class-based approach
    print("\n[Example 1: Class-Based Prediction]")
    print("-" * 70)
    
    # Initialize the model
    diet_model = DietRecommendationModel(model_dir="models")
    
    # Load saved models
    if diet_model.load_models():
        
        # Example user input
        sample_input = {
            "calories": 150.0,
            "protein": 5.0,
            "fat": 2.5,
            "carbs": 25.0,
            "fiber": 3.0,
            "sugar": 8.0,
            "sodium": 120.0,
            "user_goal": 1  # Encoded user goal (e.g., weight loss, muscle gain)
        }
        
        # Make prediction
        result = diet_model.predict(sample_input)
        
        # Display result
        if result and result["status"] == "success":
            print(f"\n✅ Prediction Result:")
            print(f"   Recommended Category: {result['predicted_category']}")
            print(f"   Confidence: {result['confidence_percentage']}%")
            print(f"   Message: {result['message']}")
        else:
            print(f"\n❌ Prediction failed: {result}")
    
    # Example 2: Using the convenience function
    print("\n\n[Example 2: Quick Prediction Function]")
    print("-" * 70)
    
    sample_input_2 = {
        "calories": 200.0,
        "protein": 15.0,
        "fat": 5.0,
        "carbs": 20.0,
        "fiber": 2.0,
        "sugar": 5.0,
        "sodium": 200.0,
        "user_goal": 2
    }
    
    result_2 = get_food_recommendation(sample_input_2)
    
    if result_2 and result_2["status"] == "success":
        print(f"\n✅ Quick Prediction:")
        print(f"   Category: {result_2['predicted_category']}")
        print(f"   Confidence: {result_2['confidence_percentage']}%")
    
    # Example 3: PostgreSQL Database Integration
    print("\n\n[Example 3: PostgreSQL Database Integration]")
    print("-" * 70)
    print("Note: This requires active PostgreSQL DB connection and valid credentials")
    
    # Configure database connection
    db_config = DatabaseConfig(
        username="SYSTEM",
        password="your_password",
        host="localhost",
        port=1521,
        service_name="XE"
    )
    
    # Example: Generate recommendation from database for user_id = 1
    # Uncomment the following lines when DB is ready:
    """
    postgres_system = PostgreSQLDietRecommendationSystem(db_config, model_dir="models")
    
    if postgres_system.connect_to_database():
        recommendation = postgres_system.generate_and_save_recommendation(user_id=1)
        
        if recommendation and recommendation["status"] == "success":
            print(f"\n✅ PostgreSQL DB Recommendation:")
            print(f"   User ID: {recommendation['user_id']}")
            print(f"   Predicted Category: {recommendation['predicted_category']}")
            print(f"   Confidence: {recommendation['confidence_percentage']}%")
            print(f"   Saved to DB: {recommendation['db_saved']}")
            print(f"   Timestamp: {recommendation['timestamp']}")
        else:
            print(f"\n❌ Recommendation failed: {recommendation}")
        
        postgres_system.disconnect_from_database()
    """
    
    print("\n" + "="*70)
    print("Module ready for integration with database and UI!")
    print("="*70)
    print("\nFeatures:")
    print("✅ Standalone ML predictions")
    print("✅ PostgreSQL Database integration")
    print("✅ Complete recommendation pipeline")
    print("✅ Error handling and logging")
    print("✅ Production-ready code")
    print("="*70)
