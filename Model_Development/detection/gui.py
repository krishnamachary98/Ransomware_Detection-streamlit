# 🖥️ Ransomware Detection GUI
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path

# Add parent directory to path to import detector
sys.path.append(str(Path(__file__).parent))
from detector import RansomwareDetector

class RansomwareDetectionGUI:
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("🔍 Ransomware Detection System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize detector
        self.detector = RansomwareDetector()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load model in background
        threading.Thread(target=self.load_model_background, daemon=True).start()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🔍 Ransomware Detection System", 
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File selection frame
        file_frame = tk.LabelFrame(main_frame, text="📁 File Selection", font=("Arial", 12, "bold"), bg='#f0f0f0')
        file_frame.pack(fill=tk.X, pady=10)
        
        # File path entry
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, font=("Arial", 10), width=60)
        file_entry.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Browse button
        browse_btn = tk.Button(
            file_frame, 
            text="📂 Browse", 
            command=self.browse_file,
            font=("Arial", 10),
            bg='#3498db',
            fg='white',
            padx=15
        )
        browse_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Analyze button
        analyze_btn = tk.Button(
            file_frame, 
            text="🔍 Analyze", 
            command=self.analyze_file,
            font=("Arial", 10, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20
        )
        analyze_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Status frame
        status_frame = tk.LabelFrame(main_frame, text="📊 Status", font=("Arial", 12, "bold"), bg='#f0f0f0')
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            status_frame, 
            text="🔄 Loading model...", 
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.status_label.pack(padx=10, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Results frame
        results_frame = tk.LabelFrame(main_frame, text="📈 Analysis Results", font=("Arial", 12, "bold"), bg='#f0f0f0')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Results text area
        self.results_text = tk.Text(results_frame, font=("Courier", 10), bg='#2c3e50', fg='white', height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar for results
        scrollbar = tk.Scrollbar(self.results_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_text.yview)
        
        # Bottom frame with model info
        info_frame = tk.Frame(self.root, bg='#34495e', height=50)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.model_info_label = tk.Label(
            info_frame, 
            text="Model: Loading...", 
            font=("Arial", 9),
            bg='#34495e',
            fg='white'
        )
        self.model_info_label.pack(pady=15)
    
    def load_model_background(self):
        """Load model in background thread"""
        try:
            success = self.detector.load_model()
            if success:
                self.update_status("✅ Model loaded successfully!", "green")
                self.update_model_info("Model: Random Forest - Ready for analysis")
            else:
                self.update_status("❌ Failed to load model", "red")
                self.update_model_info("Model: Not loaded - Check model files")
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", "red")
            self.update_model_info("Model: Error loading")
    
    def browse_file(self):
        """Open file dialog to select file"""
        file_path = filedialog.askopenfilename(
            title="Select File to Analyze",
            filetypes=[("All Files", "*.*"), ("Executable Files", "*.exe"), ("DLL Files", "*.dll")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.clear_results()
    
    def analyze_file(self):
        """Analyze the selected file"""
        file_path = self.file_path_var.get().strip()
        
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file to analyze!")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        if not self.detector.model:
            messagebox.showerror("Error", "Model not loaded! Please wait for model to load.")
            return
        
        # Start analysis in background thread
        self.update_status("🔄 Analyzing file...", "blue")
        self.progress.start()
        
        threading.Thread(target=self.analyze_file_thread, args=(file_path,), daemon=True).start()
    
    def analyze_file_thread(self, file_path):
        """Analyze file in background thread"""
        try:
            prediction, probability = self.detector.predict(file_path)
            
            if prediction is not None:
                family = self.detector.get_family_name(prediction)
                confidence = max(probability) * 100
                
                # Format results
                results = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🔍 RANSOMWARE ANALYSIS RESULTS               ║
╚══════════════════════════════════════════════════════════════╝

📁 File Information:
   • Path: {file_path}
   • Size: {os.path.getsize(file_path):,} bytes
   • Name: {os.path.basename(file_path)}

🎯 Detection Results:
   • Family: {family}
   • Confidence: {confidence:.2f}%
   • Risk Level: {"⚠️ HIGH RISK" if prediction != 0 else "✅ SAFE"}

📊 Probability Distribution:
"""
                
                # Add probability details
                families = ["Benign", "Cerber", "Locky", "WannaCry", "Petya", "CryptoLocker"]
                for i, (family_name, prob) in enumerate(zip(families, probability)):
                    bar = "█" * int(prob * 20)
                    results += f"   • {family_name:12}: {prob*100:5.1f}% |{bar:<20}|\n"
                
                results += f"""
🔒 Recommendation:
"""
                if prediction == 0:
                    results += "   ✅ File appears to be benign. No action needed."
                else:
                    results += f"   ⚠️ WARNING: File detected as {family} ransomware!\n"
                    results += "   🚫 Immediate action recommended:\n"
                    results += "      • Quarantine the file\n"
                    results += "      • Scan with antivirus\n"
                    results += "      • Do not execute the file"
                
                results += "\n" + "="*60 + "\n"
                
                self.update_results(results)
                self.update_status(f"✅ Analysis complete - {family} detected", "green" if prediction == 0 else "red")
            else:
                self.update_results("❌ Failed to analyze file. Please try again.")
                self.update_status("❌ Analysis failed", "red")
                
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            self.update_results(error_msg)
            self.update_status("❌ Analysis error", "red")
        
        finally:
            self.progress.stop()
    
    def update_status(self, message, color="black"):
        """Update status label"""
        self.root.after(0, lambda: self.status_label.config(text=message, fg=color))
    
    def update_model_info(self, message):
        """Update model info label"""
        self.root.after(0, lambda: self.model_info_label.config(text=message))
    
    def update_results(self, text):
        """Update results text area"""
        self.root.after(0, lambda: self.results_text.delete(1.0, tk.END) or self.results_text.insert(1.0, text))
    
    def clear_results(self):
        """Clear results text area"""
        self.results_text.delete(1.0, tk.END)

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = RansomwareDetectionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
