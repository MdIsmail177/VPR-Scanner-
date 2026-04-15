import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re
from urllib.parse import urlparse
import os
import requests
import binascii
import base64
import getmac
import urllib
from cryptography.fernet import Fernet, InvalidToken

# ------------------ Configuration ------------------
SECRET_KEY = b"8FhseFTi7WQWwCFEef7OquvdhD1Mu6YYkzZxiCqcZPs="

# ------------------ Phishing Detector ------------------
class PhishingDetector:
    def __init__(self):
        self.suspicious_keywords = [
            'urgent', 'verify account', 'suspended', 'click here', 'winner',
            'congratulations', 'free money', 'act now', 'limited time',
            'confirm identity', 'update payment', 'security alert', 'verify now',
            'account locked', 'billing problem', 'suspended account'
        ]
        self.malicious_patterns = [
            r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',
            r'bit\.ly|tinyurl|t\.co',
            r'[a-zA-Z0-9-]+\.tk|\.ml|\.ga|\.cf',
        ]
    
    def analyze_url(self, url):
        risk_score = 0
        details = []
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            if re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', domain):
                risk_score += 40
                details.append("Using IP address instead of domain name")
            for pattern in self.malicious_patterns:
                if re.search(pattern, domain, re.IGNORECASE):
                    risk_score += 30
                    details.append("Suspicious domain pattern detected")
            if len(url) > 100:
                risk_score += 20
                details.append("Unusually long URL")
            if domain.count('.') > 3:
                risk_score += 25
                details.append("Multiple subdomains detected")
            url_lower = url.lower()
            for word in ['secure', 'account', 'verify', 'update', 'confirm', 'login']:
                if word in url_lower and domain not in ['paypal.com', 'amazon.com', 'google.com']:
                    risk_score += 15
                    details.append(f"Suspicious keyword in URL: {word}")
            if not url.startswith('https://'):
                risk_score += 20
                details.append("Not using secure HTTPS connection")
            threat_level = "HIGH" if risk_score >= 70 else "MEDIUM" if risk_score >= 40 else "LOW"
            return {
                'risk_score': min(risk_score, 100),
                'threat_level': threat_level,
                'details': details,
                'is_safe': risk_score < 30,
                'url': url
            }
        except Exception as e:
            return {
                'risk_score': 50,
                'threat_level': "UNKNOWN",
                'details': [f"Analysis error: {str(e)}"],
                'is_safe': False,
                'url': url
            }

# ------------------ Ransomware Detector ------------------
class RansomwareDetector:
    def __init__(self):
        self.suspicious_extensions = [
            '.encrypted', '.locked', '.crypto', '.crypt', '.enc', '.zzz',
            '.aaa', '.abc', '.xyz', '.rrk', '.btc', '.wallet', '.locky'
        ]
    
    def analyze_file(self, filepath):
        filename = filepath.lower()
        for ext in self.suspicious_extensions:
            if filename.endswith(ext):
                return {
                    'file': filepath,
                    'suspicious': True,
                    'reason': f"Suspicious extension detected: {ext}"
                }
        return {
            'file': filepath,
            'suspicious': False,
            'reason': "No suspicious extension found"
        }

# ------------------ File Recovery (Improved Decryptor) ------------------
class Decryptor:
    def __init__(self):
        self.fernet = Fernet(SECRET_KEY)
    
    def decrypt_file(self, file_path):
        """Decrypt a single .locked file using Fernet encryption"""
        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Create output path
            if file_path.endswith(".locked"):
                recovered_path = file_path[:-7] + "_recovered"
            else:
                recovered_path = file_path + "_recovered"
            
            # Handle duplicate filenames
            original_path = recovered_path
            counter = 1
            while os.path.exists(recovered_path):
                name, ext = os.path.splitext(original_path)
                recovered_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Write decrypted data to file
            with open(recovered_path, "wb") as f:
                f.write(decrypted_data)
            
            return True, recovered_path
            
        except FileNotFoundError:
            return False, "File not found"
        except InvalidToken:
            return False, "Invalid decryption key - file may not be encrypted with this tool"
        except Exception as e:
            return False, f"Decryption error: {str(e)}"
    
    def decrypt_directory(self, directory_path):
        """Decrypt all .locked files in a directory"""
        results = []
        files_processed = 0
        files_recovered = 0
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.lower().endswith(".locked"):
                        full_path = os.path.join(root, file)
                        files_processed += 1
                        
                        success, result = self.decrypt_file(full_path)
                        if success:
                            files_recovered += 1
                            results.append(f"✅ Recovered: {file} -> {os.path.basename(result)}")
                        else:
                            results.append(f"❌ Failed: {file} - {result}")
            
            if files_processed == 0:
                return False, "No .locked files found in the selected directory"
            
            summary = f"\n🎉 Recovery Summary: {files_recovered}/{files_processed} files recovered successfully\n"
            return True, summary + "\n".join(results)
            
        except Exception as e:
            return False, f"Directory processing error: {str(e)}"

# ------------------ VPR Scanner Application ------------------
class VPRScanner:
    def __init__(self):
        # Initialize detectors and decryptor first
        self.detector = PhishingDetector()
        self.ransomware = RansomwareDetector()
        self.decryptor = Decryptor()
        
        # Create main window FIRST
        self.app = tk.Tk()
        
        # NOW create Tkinter variables AFTER tk.Tk()
        self.selected_file = ""
        self.recovery_mode = tk.StringVar(value="single")
        
        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        self.app.title("VPR Scanner - Cybersecurity Defense Platform")
        self.app.configure(bg="#101820")
        self.app.geometry("820x580")
        
        # Title
        title = tk.Label(self.app, text="VPR SCANNER",
                         font=("Impact", 32, "bold"),
                         bg="#101820", fg="#39ff14")
        title.pack(pady=16)
        
        # Tab buttons
        tabs_frame = tk.Frame(self.app, bg="#101820")
        tabs_frame.pack(pady=0)
        
        tk.Button(tabs_frame, text="Phishing Scanner", font=("Consolas", 14, "bold"),
                  bg="#00eaff", fg="#101820", relief="flat", 
                  command=self.show_phishing_tab).grid(row=0, column=0, padx=6)
        tk.Button(tabs_frame, text="Ransomware Scanner", font=("Consolas", 14, "bold"),
                  bg="#fc466b", fg="#101820", relief="flat", 
                  command=self.show_ransom_tab).grid(row=0, column=1, padx=6)
        tk.Button(tabs_frame, text="File Recovery", font=("Consolas", 14, "bold"),
                  bg="#29e673", fg="#101820", relief="flat", 
                  command=self.show_recovery_tab).grid(row=0, column=2, padx=6)
        
        # Container for tab content
        self.container = tk.Frame(self.app, bg="#101820")
        self.container.pack(fill="both", expand=True)
        
        # Start with phishing tab
        self.show_phishing_tab()

    def clear_tab(self):
        for widget in self.container.winfo_children():
            widget.destroy()
            
    # ---- PHISHING SCANNER TAB ----
    def show_phishing_tab(self):
        self.clear_tab()
        
        frame = tk.Frame(self.container, bg="#272834", bd=2, relief="ridge")
        frame.pack(pady=16, padx=16, fill="both", expand=True)
        
        label = tk.Label(frame, text="Enter URL to Scan:",
                        font=("Consolas", 14, "bold"),
                        bg="#272834", fg="#00eaff")
        label.pack(pady=(8,3))
        
        self.url_entry = tk.Entry(frame, font=("Consolas", 12), width=48, 
                                 bg="#21213b", fg="#ffffff")
        self.url_entry.pack(pady=7)
        
        scan_btn = tk.Button(frame, text="SCAN URL", font=("Consolas", 13, "bold"),
                             bg="#00eaff", fg="#21213b", width=17,
                             command=self.scan_url)
        scan_btn.pack(pady=10)
        
        res_label = tk.Label(frame, text="SCAN RESULTS:",
                             font=("Consolas", 12, "bold"),
                             bg="#272834", fg="#39ff14")
        res_label.pack(pady=(13,0))
        
        self.phishing_results = scrolledtext.ScrolledText(frame, font=("Consolas", 10),
                                                         width=82, height=11,
                                                         bg="#21213b", fg="#ffffff")
        self.phishing_results.pack(pady=8, padx=6, fill="both", expand=True)
    
    def scan_url(self):
        self.phishing_results.delete('1.0', tk.END)
        url = self.url_entry.get().strip()
        if not url:
            self.phishing_results.insert(tk.END, "❌ Please enter a URL to scan.\n")
            return
            
        self.phishing_results.insert(tk.END, "🔍 Scanning URL...\n" + "="*60 + "\n\n")
        result = self.detector.analyze_url(url)
        
        if result['is_safe']:
            self.phishing_results.config(fg="#00ff00")
            status_color = "🟢"
            safety_status = "✅ SECURE"
            recommendation = "✅ RECOMMENDATION: This URL is SAFE to visit.\n"
        else:
            self.phishing_results.config(fg="#ff4444")
            status_color = "🔴"
            safety_status = "❌ INSECURE"
            recommendation = "⚠️ RECOMMENDATION: This URL is UNSAFE! Exercise extreme caution.\n"
            
        self.phishing_results.insert(tk.END, f"🌐 URL: {result['url']}\n")
        self.phishing_results.insert(tk.END, f"{status_color} Status: {safety_status}\n")
        self.phishing_results.insert(tk.END, f"⚠️ Threat Level: {result['threat_level']}\n")
        self.phishing_results.insert(tk.END, f"📊 Risk Score: {result['risk_score']}/100\n\n")
        
        if result['details']:
            self.phishing_results.insert(tk.END, "📋 ANALYSIS DETAILS:\n")
            self.phishing_results.insert(tk.END, "-" * 40 + "\n")
            for detail in result['details']:
                self.phishing_results.insert(tk.END, f"• {detail}\n")
                
        self.phishing_results.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.phishing_results.insert(tk.END, recommendation)
    
    # ---- RANSOMWARE SCANNER TAB ----
    def show_ransom_tab(self):
        self.clear_tab()
        
        frame = tk.Frame(self.container, bg="#272834", bd=2, relief="ridge")
        frame.pack(pady=16, padx=16, fill="both", expand=True)
        
        label = tk.Label(frame, text="Select File to Scan:",
                         font=("Consolas", 14, "bold"), bg="#272834", fg="#fc466b")
        label.pack(pady=(10,6))
        
        select_btn = tk.Button(frame, text="SELECT FILE", font=("Consolas", 13, "bold"),
                              bg="#fc466b", fg="#ffffff", width=17,
                              command=self.scan_file)
        select_btn.pack(pady=7)
        
        res_label = tk.Label(frame, text="SCAN RESULTS:",
                             font=("Consolas", 12, "bold"),
                             bg="#272834", fg="#39ff14")
        res_label.pack(pady=(14,0))
        
        self.ransomware_results = scrolledtext.ScrolledText(frame, font=("Consolas", 10),
                                                           width=82, height=11,
                                                           bg="#21213b", fg="#ffffff")
        self.ransomware_results.pack(pady=8, padx=6, fill="both", expand=True)
    
    def scan_file(self):
        self.ransomware_results.delete('1.0', tk.END)
        filepath = filedialog.askopenfilename(title="Select file to scan", 
                                            filetypes=[("All files", "*.*")])
        if not filepath:
            return
            
        self.ransomware_results.insert(tk.END, "🔍 Scanning file...\n" + "="*60 + "\n\n")
        result = self.ransomware.analyze_file(filepath)
        
        if not result['suspicious']:
            self.ransomware_results.config(fg="#00ff00")
            status_color = "🟢"
            safety_status = "✅ SECURE"
            recommendation = "✅ RECOMMENDATION: File appears to be CLEAN and SAFE.\n"
        else:
            self.ransomware_results.config(fg="#ff4444")
            status_color = "🔴"
            safety_status = "❌ SUSPICIOUS"
            recommendation = "⚠️ RECOMMENDATION: This file may be infected with RANSOMWARE!\n🛡️ Quarantine this file immediately and run a full system scan.\n"
            
        self.ransomware_results.insert(tk.END, f"📁 File: {result['file']}\n")
        self.ransomware_results.insert(tk.END, f"{status_color} Status: {safety_status}\n")
        self.ransomware_results.insert(tk.END, f"📝 Analysis: {result['reason']}\n\n")
        self.ransomware_results.insert(tk.END, "=" * 60 + "\n")
        self.ransomware_results.insert(tk.END, recommendation)

    # ---- FILE RECOVERY TAB ----
    def show_recovery_tab(self):
        self.clear_tab()
        
        frame = tk.Frame(self.container, bg="#272834", bd=2, relief="ridge")
        frame.pack(pady=16, padx=16, fill="both", expand=True)
        
        # Recovery mode selection
        mode_frame = tk.Frame(frame, bg="#272834")
        mode_frame.pack(pady=(10,0), padx=10, fill="x")
        
        mode_label = tk.Label(mode_frame, text="Recovery Mode:",
                              font=("Consolas", 14, "bold"), bg="#272834", fg="#29e673")
        mode_label.pack(side="left")
        
        tk.Radiobutton(mode_frame, text="Single File", variable=self.recovery_mode, value="single",
                       font=("Consolas", 12), bg="#272834", fg="#00eaff", 
                       activebackground="#272834", selectcolor="#272834").pack(side="left", padx=(20,10))
        tk.Radiobutton(mode_frame, text="Entire Directory", variable=self.recovery_mode, value="directory",
                       font=("Consolas", 12), bg="#272834", fg="#00eaff", 
                       activebackground="#272834", selectcolor="#272834").pack(side="left", padx=10)

        # File selection
        select_frame = tk.Frame(frame, bg="#272834")
        select_frame.pack(pady=(15,5), padx=10, fill="x")
        
        select_label = tk.Label(select_frame, text="Select encrypted file/folder:",
                                font=("Consolas", 13, "bold"), bg="#272834", fg="#00eaff")
        select_label.pack(side="left")
        
        choose_btn = tk.Button(select_frame, text="CHOOSE",
                               font=("Consolas", 13, "bold"), bg="#fc466b", fg="white",
                               command=self.choose_file)
        choose_btn.pack(side="right")
        
        # File path display
        self.file_path_label = tk.Label(frame, text="No file/folder selected",
                                       font=("Consolas", 11), bg="#272834", fg="#a2a2a2", 
                                       wraplength=700, justify="left")
        self.file_path_label.pack(pady=(0,10), padx=10, fill="x")

        # Recover button
        recover_btn = tk.Button(frame, text="RECOVER FILES",
                                font=("Consolas", 13, "bold"), bg="#29e673", fg="white",
                                command=self.recover_file)
        recover_btn.pack(pady=(5,8))
        
        # Results area
        res_label = tk.Label(frame, text="RECOVERY RESULTS:",
                             font=("Consolas", 12, "bold"),
                             bg="#272834", fg="#29e673")
        res_label.pack(pady=(6,0), padx=10, anchor="w")
        
        self.recovery_results = scrolledtext.ScrolledText(frame, font=("Consolas", 10),
                                                         width=82, height=10,
                                                         bg="#21213b", fg="#ffffff")
        self.recovery_results.pack(pady=6, padx=10, fill="both", expand=True)

    def choose_file(self):
        if self.recovery_mode.get() == "single":
            file_path = filedialog.askopenfilename(
                title="Select locked/encrypted file",
                filetypes=[("Locked files", "*.locked"), ("All files", "*.*")]
            )
            if file_path:
                self.selected_file = file_path
                self.file_path_label.config(text=f"Selected file: {file_path}")
            else:
                self.selected_file = ""
                self.file_path_label.config(text="No file selected")
        else:
            dir_path = filedialog.askdirectory(title="Select directory containing locked files")
            if dir_path:
                self.selected_file = dir_path
                self.file_path_label.config(text=f"Selected directory: {dir_path}")
            else:
                self.selected_file = ""
                self.file_path_label.config(text="No directory selected")

    def recover_file(self):
        self.recovery_results.delete('1.0', tk.END)
        path = self.selected_file
        
        if not path:
            self.recovery_results.insert(tk.END, "❌ Please choose a file or directory to recover.\n")
            return
            
        mode = self.recovery_mode.get()
        
        try:
            if mode == "single":
                self.recovery_results.insert(tk.END, "🔍 Recovering file...\n" + "="*60 + "\n\n")
                success, result = self.decryptor.decrypt_file(path)
                
                if success:
                    self.recovery_results.config(fg="#00ff00")
                    self.recovery_results.insert(tk.END, f"✅ SUCCESS! File recovered successfully!\n\n")
                    self.recovery_results.insert(tk.END, f"📁 Original file: {os.path.basename(path)}\n")
                    self.recovery_results.insert(tk.END, f"💾 Recovered file: {os.path.basename(result)}\n")
                    self.recovery_results.insert(tk.END, f"📂 Location: {os.path.dirname(result)}\n\n")
                    self.recovery_results.insert(tk.END, "🎉 Your file has been successfully decrypted and recovered!")
                else:
                    self.recovery_results.config(fg="#ff4444")
                    self.recovery_results.insert(tk.END, f"❌ RECOVERY FAILED\n\n")
                    self.recovery_results.insert(tk.END, f"📝 Error details: {result}\n\n")
                    self.recovery_results.insert(tk.END, "💡 Make sure the file is encrypted with this tool and not corrupted.")
                    
            else:  # Directory mode
                self.recovery_results.insert(tk.END, "🔍 Recovering directory...\n" + "="*60 + "\n\n")
                success, result = self.decryptor.decrypt_directory(path)
                
                if success:
                    self.recovery_results.config(fg="#00ff00")
                    self.recovery_results.insert(tk.END, result)
                else:
                    self.recovery_results.config(fg="#ff4444")
                    self.recovery_results.insert(tk.END, f"❌ DIRECTORY RECOVERY FAILED\n\n")
                    self.recovery_results.insert(tk.END, f"📝 Error details: {result}")
                    
        except Exception as e:
            self.recovery_results.config(fg="#ff4444")
            self.recovery_results.insert(tk.END, f"❌ UNEXPECTED ERROR\n\n")
            self.recovery_results.insert(tk.END, f"📝 Error details: {str(e)}\n\n")
            self.recovery_results.insert(tk.END, "💡 Please try again or contact support if the problem persists.")

    def run(self):
        self.app.mainloop()

# ------------------ Run Application ------------------
if __name__ == "__main__":
    scanner = VPRScanner()
    scanner.run()