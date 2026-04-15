#!/usr/bin/env python3
"""
VPR Scanner GUI - Virus, Phishing, Ransomware Detection & File Recovery
Compatible with static SECRET_KEY ransomware simulation.
"""

import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, StringVar
from urllib.parse import urlparse
from cryptography.fernet import Fernet, InvalidToken

SECRET_KEY =DknSBkLeS2sbfTDphCktFGkmutKf66oyvN8bpTxfBxg=

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
        risk_score, details = 0, []
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

class Decryptor:
    def __init__(self):
        self.fernet = Fernet(SECRET_KEY)
    
    def decrypt_file(self, file_path):
        encrypted_path = file_path
        # Handle user selecting original (ransom note) file: look for its backup first
        if not (file_path.endswith(".encrypted") or file_path.endswith(".locked")):
            candidate = file_path + ".encrypted"
            if os.path.exists(candidate):
                encrypted_path = candidate
            else:
                candidate = file_path + ".locked"
                if os.path.exists(candidate):
                    encrypted_path = candidate
                else:
                    return False, "Select a .encrypted or .locked file, not ransom note"
        try:
            with open(encrypted_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            recovered_path = encrypted_path.rsplit(".", 1)[0] + "_recovered"
            orig = recovered_path
            counter = 1
            while os.path.exists(recovered_path):
                name, ext = os.path.splitext(orig)
                recovered_path = f"{name}_{counter}{ext}"
                counter += 1
            with open(recovered_path, "wb") as f:
                f.write(decrypted_data)
            return True, recovered_path
        except FileNotFoundError:
            return False, "File not found"
        except InvalidToken:
            return False, "Invalid decryption key or file not encrypted with this tool"
        except Exception as e:
            return False, f"Decryption error: {str(e)}"
    
    def decrypt_directory(self, directory_path):
        results = []
        files_processed, files_recovered = 0, 0
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith(".encrypted") or file.endswith(".locked"):
                        full_path = os.path.join(root, file)
                        files_processed += 1
                        success, result = self.decrypt_file(full_path)
                        if success:
                            files_recovered += 1
                            results.append(f"✅ Recovered: {file} -> {os.path.basename(result)}")
                        else:
                            results.append(f"❌ Failed: {file} - {result}")
            if files_processed == 0:
                return False, "No .encrypted or .locked files found"
            summary = f"\n🎉 Recovery Summary: {files_recovered}/{files_processed} files recovered\n"
            return True, summary + "\n".join(results)
        except Exception as e:
            return False, f"Directory processing error: {str(e)}"

class AppLogic:
    def __init__(self):
        self.detector = PhishingDetector()
        self.ransomware = RansomwareDetector()
        self.decryptor = Decryptor()
        self.selected_file = ""

    def scan_url(self, url_entry, results_widget):
        results_widget.delete('1.0', 'end')
        url = url_entry.get().strip()
        if not url:
            results_widget.insert('end', "❌ Please enter a URL to scan.\n")
            return
        results_widget.insert('end', "🔍 Scanning URL...\n" + "="*60 + "\n\n")
        result = self.detector.analyze_url(url)
        if result['is_safe']:
            results_widget.config(fg="#00ff00")
            status_color = "🟢"
            safety_status = "✅ SECURE"
            recommendation = "✅ RECOMMENDATION: This URL is SAFE to visit.\n"
        else:
            results_widget.config(fg="#ff4444")
            status_color = "🔴"
            safety_status = "❌ INSECURE"
            recommendation = "⚠️ RECOMMENDATION: This URL is UNSAFE! Exercise extreme caution.\n"
        results_widget.insert('end', f"🌐 URL: {result['url']}\n")
        results_widget.insert('end', f"{status_color} Status: {safety_status}\n")
        results_widget.insert('end', f"⚠️ Threat Level: {result['threat_level']}\n")
        results_widget.insert('end', f"📊 Risk Score: {result['risk_score']}/100\n\n")
        if result['details']:
            results_widget.insert('end', "📋 ANALYSIS DETAILS:\n")
            results_widget.insert('end', "-" * 40 + "\n")
            for detail in result['details']:
                results_widget.insert('end', f"• {detail}\n")
        results_widget.insert('end', "\n" + "=" * 60 + "\n")
        results_widget.insert('end', recommendation)

    def scan_file(self, results_widget):
        results_widget.delete('1.0', 'end')
        filepath = filedialog.askopenfilename(title="Select file to scan")
        if not filepath:
            return
        results_widget.insert('end', "🔍 Scanning file...\n" + "="*60 + "\n\n")
        result = self.ransomware.analyze_file(filepath)
        if not result['suspicious']:
            results_widget.config(fg="#00ff00")
            status_color = "🟢"
            safety_status = "✅ SECURE"
            recommendation = "✅ RECOMMENDATION: File appears to be CLEAN and SAFE.\n"
        else:
            results_widget.config(fg="#ff4444")
            status_color = "🔴"
            safety_status = "❌ SUSPICIOUS"
            recommendation = "⚠️ RECOMMENDATION: This file may be infected with RANSOMWARE!\n🛡️ Quarantine this file immediately.\n"
        results_widget.insert('end', f"📁 File: {result['file']}\n")
        results_widget.insert('end', f"{status_color} Status: {safety_status}\n")
        results_widget.insert('end', f"📝 Analysis: {result['reason']}\n\n")
        results_widget.insert('end', "=" * 60 + "\n")
        results_widget.insert('end', recommendation)

    def choose_file(self, recovery_mode_var, file_path_label):
        if recovery_mode_var.get() == "single":
            file_path = filedialog.askopenfilename(
                title="Select .encrypted/.locked file",
                filetypes=[("Encrypted files", "*.encrypted"), ("Locked files", "*.locked"), ("All files", "*.*")]
            )
            if file_path:
                self.selected_file = file_path
                file_path_label.config(text=f"Selected file: {file_path}")
            else:
                self.selected_file = ""
                file_path_label.config(text="No file selected")
        else:
            dir_path = filedialog.askdirectory(title="Select directory with .encrypted/.locked files")
            if dir_path:
                self.selected_file = dir_path
                file_path_label.config(text=f"Selected directory: {dir_path}")
            else:
                self.selected_file = ""
                file_path_label.config(text="No directory selected")

    def recover_file(self, recovery_mode_var, results_widget):
        results_widget.delete('1.0', 'end')
        path = self.selected_file
        if not path:
            results_widget.insert('end', "❌ Please choose a valid .encrypted/.locked file or directory.\n")
            return
        mode = recovery_mode_var.get()
        try:
            if mode == "single":
                results_widget.insert('end', "🔍 Recovering file...\n" + "="*60 + "\n\n")
                success, result = self.decryptor.decrypt_file(path)
                if success:
                    results_widget.config(fg="#00ff00")
                    results_widget.insert('end', f"✅ SUCCESS! File recovered: {result}\n")
                else:
                    results_widget.config(fg="#ff4444")
                    results_widget.insert('end', f"❌ RECOVERY FAILED: {result}\n")
                    results_widget.insert('end', "💡 Ensure you're selecting an encrypted file, not ransom note.")
            else:
                results_widget.insert('end', "🔍 Recovering directory...\n" + "="*60 + "\n\n")
                success, result = self.decryptor.decrypt_directory(path)
                if success:
                    results_widget.config(fg="#00ff00")
                    results_widget.insert('end', result)
                else:
                    results_widget.config(fg="#ff4444")
                    results_widget.insert('end', f"❌ DIRECTORY RECOVERY FAILED: {result}\n")
        except Exception as e:
            results_widget.config(fg="#ff4444")
            results_widget.insert('end', f"❌ UNEXPECTED ERROR: {str(e)}\n")

def main():
    root = tk.Tk()
    root.title('VPR Scanner')
    root.geometry("800x620")
    app = AppLogic()
    style = ttk.Style()
    style.theme_use('clam')

    app_frame = tk.Frame(root, bg="#111")
    app_frame.pack(fill="both", expand=True, padx=8, pady=8)

    notebook = ttk.Notebook(app_frame)
    notebook.pack(fill="both", expand=True)

    # PHISHING TAB
    phishing_tab = ttk.Frame(notebook)
    notebook.add(phishing_tab, text="Phishing Detection")

    url_entry = tk.Entry(phishing_tab, font=("Arial", 12), width=70)
    url_entry.pack(pady=10)
    scan_url_btn = ttk.Button(phishing_tab, text="Scan URL", command=lambda: app.scan_url(url_entry, phishing_results))
    scan_url_btn.pack(pady=6)

    phishing_results = scrolledtext.ScrolledText(phishing_tab, height=16, font=("Consolas", 10), fg="#00ff00", bg="#222")
    phishing_results.pack(fill="both", expand=True, padx=10, pady=10)

    # RANSOMWARE TAB
    ransomware_tab = ttk.Frame(notebook)
    notebook.add(ransomware_tab, text="Ransomware Detection")

    scan_file_btn = ttk.Button(ransomware_tab, text="Scan File", command=lambda: app.scan_file(ransomware_results))
    scan_file_btn.pack(pady=10)
    ransomware_results = scrolledtext.ScrolledText(ransomware_tab, height=16, font=("Consolas", 10), fg="#00ff00", bg="#222")
    ransomware_results.pack(fill="both", expand=True, padx=10, pady=10)

    # RECOVERY TAB
    recovery_tab = ttk.Frame(notebook)
    notebook.add(recovery_tab, text="File Recovery")

    mode_var = StringVar(value="single")
    radio_frame = tk.Frame(recovery_tab, bg="#222")
    radio_frame.pack(pady=10)
    ttk.Radiobutton(radio_frame, text="Single File", variable=mode_var, value="single").pack(side="left", padx=16)
    ttk.Radiobutton(radio_frame, text="Directory", variable=mode_var, value="directory").pack(side="left", padx=16)

    file_path_label = tk.Label(recovery_tab, text="No file/directory selected", bg="#222", fg="#fff", font=("Arial", 11))
    file_path_label.pack(pady=8)
    choose_btn = ttk.Button(recovery_tab, text="Choose", command=lambda: app.choose_file(mode_var, file_path_label))
    choose_btn.pack(pady=6)

    recover_btn = ttk.Button(recovery_tab, text="Recover Files", command=lambda: app.recover_file(mode_var, recovery_results))
    recover_btn.pack(pady=8)
    recovery_results = scrolledtext.ScrolledText(recovery_tab, height=15, font=("Consolas", 10), fg="#ff4444", bg="#222")
    recovery_results.pack(fill="both", expand=True, padx=10, pady=16)

    root.mainloop()

if __name__ == "__main__":
    main()