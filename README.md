# 🛡️ Ransomware Detection System

A machine learning-based ransomware detection system with both desktop and web interfaces.

## 📊 Model Performance
- **Accuracy**: 92.59%
- **Algorithm**: Random Forest
- **Features**: 1024 binary header features
- **Families**: 26 ransomware families + Benign
- **Training Samples**: 2,157 files

## 🚀 Quick Start

### Option 1: Desktop GUI (Tkinter)
```bash
cd Model_Development/detection
python gui.py
```

### Option 2: Web Interface (Streamlit)
```bash
cd Model_Development/detection
streamlit run streamlit.py
```

### Option 3: Command Line
```bash
cd Model_Development/detection
python detector.py
```

## 📁 Project Structure

```
my_project/
├── Model_Development/
│   ├── Data/
│   │   └── Ransomware_headers.csv          # Training dataset
│   ├── models/
│   │   ├── ransomware_rf_model.pkl         # Trained model
│   │   └── feature_columns.pkl             # Feature names
│   ├── detection/
│   │   ├── detector.py                     # Core detection logic
│   │   ├── gui.py                          # Desktop GUI
│   │   ├── streamlit.py                    # Web interface
│   │   └── run_gui.py                      # GUI launcher
│   └── random_forest_training.py          # Model training script
├── EDA/
│   └── data_size_reducer.ipynb            # Data reduction notebook
└── README.md
```

## 🔧 Setup

1. **Install Dependencies**
```bash
pip install pandas numpy scikit-learn streamlit tkinter
```

2. **Train Model** (if not already trained)
```bash
cd Model_Development
python random_forest_training.py
```

## 🎯 Features

- **Multi-Interface**: Desktop GUI and Web interface
- **Real-time Analysis**: Fast file scanning (<3 seconds)
- **Family Detection**: Identifies 26 different ransomware families
- **Confidence Scores**: Probability-based predictions
- **File Type Support**: Analyzes any file type
- **Risk Assessment**: Clear safety recommendations

## 📋 Supported Ransomware Families

- Benign
- Cerber
- Locky
- WannaCry
- Petya
- CryptoLocker
- And 20+ other variants

## ⚠️ Important Notes

- For educational and research purposes only
- Not a replacement for professional antivirus software
- Always verify results with multiple security tools

## 🤖 Model Details

The Random Forest classifier analyzes the first 1024 bytes of files to detect ransomware signatures and patterns. The model was trained on a diverse dataset of ransomware samples and benign files.

## 📈 Performance Metrics

- **Precision**: High precision for most families
- **Recall**: Excellent detection rates
- **False Positives**: <5% rate
- **Processing Time**: <3 seconds per file

## 🔒 Security Considerations

- Temporary files are automatically deleted
- No data is stored or transmitted
- Local processing only
- No internet connection required

## 🐛 Troubleshooting

**Model Loading Issues:**
- Ensure model files exist in `Model_Development/models/`
- Run training script if models are missing

**Import Errors:**
- Check Python path configuration
- Verify all dependencies are installed

**GUI Issues:**
- Ensure tkinter is installed
- Try running from command line

## 📞 Support

For issues or questions:
1. Check this README
2. Verify model files exist
3. Test with `detector.py` first
4. Check console output for errors

---

**⚠️ Disclaimer**: This tool is for educational purposes. Always use professional security software for real-world protection.
