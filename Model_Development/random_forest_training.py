# Random Forest Training - Ransomware Detection

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

print("Libraries loaded!")

# Load the full dataset
print("Loading full dataset (this may take a moment)...")
df = pd.read_csv('Model_Development/Data/Ransomware_headers.csv')
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns[:10])}...")  # Show first 10 columns
print(f"Family distribution:")
print(df['family'].value_counts())

# Prepare features and target
print("Preparing features...")
X = df.drop(['ID', 'filename', 'GR', 'family'], axis=1, errors='ignore')
y = df['family']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Handle any potential missing values
X = X.fillna(0)
# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train Random Forest
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

print("Training Random Forest...")
rf.fit(X_train, y_train)
print("Training completed!")

# Make predictions
y_pred = rf.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("Top 10 Important Features:")
print(feature_importance.head(10))


joblib.dump(rf, "D:/bunny/SNIST HACKATHON/my_project/Model_Development/models/ransomware_rf_model.pkl")
joblib.dump(X.columns.tolist(), "D:/bunny/SNIST HACKATHON/my_project/Model_Development/models/feature_columns.pkl")

print("Model saved successfully!")