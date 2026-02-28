# 🔍 Ransomware Detector
import pandas as pd
import numpy as np
import joblib
import os
import sys
from pathlib import Path

class RansomwareDetector:
    def __init__(self):
        """Initialize the ransomware detector"""
        self.model = None
        self.feature_columns = None
        self.model_path = Path(__file__).parent.parent / "models" / "ransomware_rf_model.pkl"
        self.features_path = Path(__file__).parent.parent / "models" / "feature_columns.pkl"
        
    def load_model(self):
        """Load the trained model and feature columns"""
        try:
            print("Loading model...")
            self.model = joblib.load(self.model_path)
            self.feature_columns = joblib.load(self.features_path)
            print("Model loaded successfully!")
            return True
        except FileNotFoundError:
            print(f"Model files not found at {self.model_path}")
            print("Please train the model first using random_forest_training.py")
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def extract_features(self, file_path):
        """Extract features from a file for prediction"""
        try:
            # Read file as binary
            with open(file_path, 'rb') as f:
                binary_data = f.read()
            
            # Extract first 1024 bytes as features
            features = {}
            for i in range(1024):
                if i < len(binary_data):
                    features[str(i)] = binary_data[i]
                else:
                    features[str(i)] = 0
            
            return features
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def predict(self, file_path):
        """Predict if a file is ransomware"""
        if not self.model:
            if not self.load_model():
                return None, None
        
        # Extract features
        features = self.extract_features(file_path)
        if features is None:
            return None, None
        
        # Create DataFrame with correct column order
        feature_df = pd.DataFrame([features])
        
        # Ensure all required columns exist
        for col in self.feature_columns:
            if col not in feature_df.columns:
                feature_df[col] = 0
        
        # Select only the columns the model was trained on
        feature_df = feature_df[self.feature_columns]
        
        # Make prediction
        try:
            prediction = self.model.predict(feature_df)[0]
            probability = self.model.predict_proba(feature_df)[0]
            
            return prediction, probability
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None, None
    
    def get_family_name(self, prediction):
        """Convert prediction number to family name"""
        family_map = {
            0: "Benign",
            1: "Cerber", 
            2: "Locky",
            3: "WannaCry",
            4: "Petya",
            5: "CryptoLocker"
        }
        return family_map.get(prediction, f"Unknown Family {prediction}")

def main():
    """Test the detector"""
    detector = RansomwareDetector()
    
    if not detector.load_model():
        return
    
    # Example usage
    file_path = input("Enter file path to analyze: ").strip()
    
    if not os.path.exists(file_path):
        print("File not found!")
        return
    
    prediction, probability = detector.predict(file_path)
    
    if prediction is not None:
        family = detector.get_family_name(prediction)
        confidence = max(probability) * 100
        
        print(f"\n🔍 Analysis Results:")
        print(f"File: {file_path}")
        print(f"Family: {family}")
        print(f"Confidence: {confidence:.2f}%")
        print(f"Probabilities: {probability}")
    else:
        print("Failed to analyze file!")

if __name__ == "__main__":
    main()
