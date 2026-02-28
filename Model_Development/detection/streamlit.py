import streamlit as st
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))
from detector import RansomwareDetector

st.set_page_config(page_title="Ransomware Detection", layout="centered")

st.title("🔍 Ransomware Detection System")

# Load model
@st.cache_resource
def load_detector():
    detector = RansomwareDetector()
    detector.load_model()
    return detector

detector = load_detector()

uploaded_file = st.file_uploader("Upload EXE or DLL file", type=["exe", "dll"])

if uploaded_file is not None:
    # Save temporary file
    temp_path = os.path.join("temp_file.exe")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Analyze file
    prediction, probability = detector.predict(temp_path)
    
    if prediction is not None:
        family_name = detector.get_family_name(prediction)
        confidence = max(probability) * 100
        
        st.subheader("Analysis Results")
        
        if family_name == "Benign":
            st.success(f"✅ File is Clean: {family_name}")
            st.info(f"Confidence: {confidence:.2f}%")
        else:
            st.error(f"⚠️ Ransomware Detected: {family_name}")
            st.warning(f"Confidence: {confidence:.2f}%")
            st.error("🚫 DO NOT EXECUTE THIS FILE!")
        
        # Show probability distribution
        st.subheader("Probability Distribution")
        prob_data = {
            "Family": [f"Family_{i}" for i in range(len(probability))],
            "Probability": probability
        }
        st.bar_chart(prob_data)
    
    # Clean up
    if os.path.exists(temp_path):
        os.remove(temp_path)
