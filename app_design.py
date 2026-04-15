
import tkinter as tk
from tkinter import filedialog, scrolledtext
import math

class AppDesign:
    def __init__(self, app_logic):
        self.app_logic = app_logic
        self.app = tk.Tk()
        self.current_page = "main"

    def setup_main_window(self):
        self.app.title("VPR Scanner - Cybersecurity Defense Platform")
        self.app.geometry("900x700")
        self.app.configure(bg="#111D2B")
        self.create_hex_background()
        
    def create_hex_background(self):
        self.bg_canvas = tk.Canvas(self.app, bg="#111D2B", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.bind("<Configure>", self._on_bg_resize)
        self._draw_hex_pattern(self.bg_canvas.winfo_width(), self.bg_canvas.winfo_height())

    def _on_bg_resize(self, event):
        self._draw_hex_pattern(event.width, event.height)

    def _draw_hex_pattern(self, width, height):
        self.bg_canvas.delete("all")
        for y in range(0, height+35, 35):
            for x in range(-40 if (y//35)%2==1 else 0, width+70, 70):
                self.draw_hexagon(self.bg_canvas, x, y, 30, outline="#202e4a", fill="#182941")
        self.bg_canvas.create_rectangle(0, int(height*0.64), width, height, fill="#223b5a", width=0)

    def draw_hexagon(self, canvas, x, y, r, outline="#ccc", fill="#182941"):
        pts = []
        for i in range(6):
            angle = (math.pi/3) * i
            pts.append(x + r * (math.cos(angle)))
            pts.append(y + r * (math.sin(angle)))
        canvas.create_polygon(pts, outline=outline, fill=fill)

    def create_glow_box(self, parent, width=540, height=430):
        frame = tk.Frame(parent, bg="#28364a", bd=0, highlightbackground="#47cdff",
                         highlightcolor="#47cdff", highlightthickness=4)
        frame.config(width=width, height=height)
        frame.pack_propagate(False)
        return frame

    def create_main_page(self):
        self.clear_window()
        self.create_hex_background()
        main_frame = tk.Frame(self.app, bg="#111D2B", width=900, height=700)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        neon_title = tk.Label(main_frame, text="VPR SCANNER",
                              font=("Stencil", 38, "bold"), bg="#111D2B", fg="#46eaff")
        neon_title.pack(pady=(45, 8))
        sub = tk.Label(main_frame, text="🛡️CYBERSECURITY DEFENSE PLATFORM  🛡️",
                       font=("Stencil", 16, "bold"), bg="#111D2B", fg="#8adeff")
        sub.pack(pady=(2,28))
        box = self.create_glow_box(main_frame, width=540, height=430)
        box.pack()
        btn_font = ("Consolas", 16, "bold")

        tk.Button(box, text="🔍 PHISHING SCANNER",
                  font=btn_font, bg="#1a375a", fg="#46eaff", activebackground="#58cbff", activeforeground="#232c39",
                  relief="solid", bd=2, width=25, height=2,
                  command=self.show_phishing_page).pack(pady=18)
        tk.Button(box, text="🛡️RANSOMWARE SCANNER",
                  font=btn_font, bg="#212141", fg="#eeaaff", activebackground="#be81ff", activeforeground="#232c39",
                  relief="solid", bd=2, width=25, height=2,
                  command=self.show_ransomware_page).pack(pady=18)
        tk.Button(box, text="💾 FILE RECOVERY",
                  font=btn_font, bg="#194055", fg="#a1ffd9", activebackground="#22cf92", activeforeground="#222b35",
                  relief="solid", bd=2, width=25, height=2,
                  command=self.show_recovery_page).pack(pady=18)

        tk.Label(main_frame, text="© 2025 VPR Scanner | Advanced Cybersecurity Defense | Next-Gen Cybersecurity for Modern Threats",
                 font=("Bahnschrift", 11, "bold"),
                 fg="#3eabe1", bg="#111D2B").pack(side="bottom", pady=(30,0))
        
    def show_phishing_page(self):
        self.current_page = "phishing"
        self.clear_window()
        self.create_hex_background()
        main_frame = tk.Frame(self.app, bg="#111D2B", width=900, height=700)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        header = tk.Label(main_frame, text="PHISHING SCANNER", font=("Stencil", 25, "bold"), bg="#111D2B", fg="#19f5d9")
        header.pack(pady=(45,15))

        back_btn = tk.Button(main_frame, text="◄ BACK",
                             font=("Consolas", 11, "bold"),
                             bg="#143345", fg="#4cf7ff", relief="solid", bd=2,
                             command=self.create_main_page)
        back_btn.place(x=40, y=30)

        box = self.create_glow_box(main_frame, width=650, height=360)
        box.pack(pady=(30, 0))
        entry_label = tk.Label(box, text="Enter URL to Scan",
                               font=("Consolas", 13, "bold"), bg="#28364a", fg="#14faaf")
        entry_label.pack(pady=(17,3))
        self.url_entry = tk.Entry(box, font=("Consolas", 12), bg="#0a2234", fg="#dbfcfc", width=54, relief="solid", bd=2,
                                  insertbackground="#47cdff")
        self.url_entry.pack(pady=(3,15))
        scan_btn = tk.Button(box, text="🔎  SCAN URL", font=("Consolas", 13, "bold"),
                             bg="#143345", fg="#30e1c6", width=18, relief="solid", bd=2,
                             activebackground="#07676d",
                             command=lambda: self.app_logic.scan_url(self.url_entry, self.phishing_results))
        scan_btn.pack(pady=5)
        res_label = tk.Label(box, text="SCAN RESULTS:",
                             font=("Consolas", 11, "bold"), bg="#28364a", fg="#73bfff")
        res_label.pack(pady=(15,3))
        self.phishing_results = scrolledtext.ScrolledText(box, font=("Consolas", 10),
                                                         width=75, height=8,
                                                         bg="#13222F", fg="#d1f9fc", insertbackground="#47cdff")
        self.phishing_results.pack(pady=(2, 16), fill="both", expand=True)

    def show_ransomware_page(self):
        self.current_page = "ransomware"
        self.clear_window()
        self.create_hex_background()
        main_frame = tk.Frame(self.app, bg="#111D2B")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        header = tk.Label(main_frame, text="RANSOMWARE SCANNER", font=("Stencil", 25, "bold"),
                          bg="#111D2B", fg="#f4aaff")
        header.pack(pady=(45,15))

        back_btn = tk.Button(main_frame, text="◄ BACK",
                             font=("Consolas", 11, "bold"),
                             bg="#241A37", fg="#eeaaff", relief="solid", bd=2,
                             command=self.create_main_page)
        back_btn.place(x=40, y=30)

        box = self.create_glow_box(main_frame, width=650, height=360)
        box.pack(pady=(30, 0))
        entry_label = tk.Label(box, text="Select File to Scan",
                               font=("Consolas", 13, "bold"), bg="#28364a", fg="#eeaaff")
        entry_label.pack(pady=(17,8))

        select_btn = tk.Button(box, text="📁 SELECT FILE",
                               font=("Consolas", 13, "bold"),
                               bg="#212141", fg="#eeaaff", width=23,
                               relief="solid", bd=2, activebackground="#be81ff",
                               command=lambda: self.app_logic.scan_file(self.ransomware_results))
        select_btn.pack(pady=8)
        res_label = tk.Label(box, text="SCAN RESULTS:",
                             font=("Consolas", 11, "bold"), bg="#28364a", fg="#ffaaff")
        res_label.pack(pady=(16,3))
        self.ransomware_results = scrolledtext.ScrolledText(box, font=("Consolas", 10),
                                                           width=75, height=8,
                                                           bg="#20133B", fg="#f4aaff")
        self.ransomware_results.pack(pady=(2, 16), fill="both", expand=True)

    def show_recovery_page(self):
        self.current_page = "recovery"
        self.clear_window()
        self.create_hex_background()
        main_frame = tk.Frame(self.app, bg="#111D2B")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        header = tk.Label(main_frame, text="FILE RECOVERY", font=("Stencil", 25, "bold"),
                          bg="#111D2B", fg="#36e1ef")
        header.pack(pady=(45,15))
        back_btn = tk.Button(main_frame, text="◄ BACK",
                             font=("Consolas", 11, "bold"),
                             bg="#194055", fg="#a1ffd9", relief="solid", bd=2,
                             command=self.create_main_page)
        back_btn.place(x=40, y=30)

        box = self.create_glow_box(main_frame, width=650, height=410)
        box.pack(pady=(30, 0))
        mode_label = tk.Label(box, text="Recovery Mode:",
                             font=("Consolas", 13, "bold"), bg="#28364a", fg="#a1ffd9")
        mode_label.pack(pady=(25,4))
        self.recovery_mode = tk.StringVar(value="single")

        tk.Radiobutton(box, text="Single File", variable=self.recovery_mode, value="single",
                      font=("Consolas", 11), bg="#28364a", fg="#30e1c6",
                      activebackground="#28364a", selectcolor="#13222F").pack(side="left", padx=(40, 5))
        tk.Radiobutton(box, text="Directory", variable=self.recovery_mode, value="directory",
                      font=("Consolas", 11), bg="#28364a", fg="#30e1c6",
                      activebackground="#28364a", selectcolor="#13222F").pack(side="left", padx=8)

        select_label = tk.Label(box, text="Select encrypted file/folder:",
                               font=("Consolas", 12, "bold"), bg="#28364a", fg="#a1ffd9")
        select_label.pack(pady=(37, 8))
        choose_btn = tk.Button(box, text="📁 CHOOSE",
                              font=("Consolas", 13, "bold"), bg="#194055", fg="#a1ffd9",
                              relief="solid", bd=2,
                              command=lambda: self.app_logic.choose_file(self.recovery_mode, self.file_path_label))
        choose_btn.pack()
        self.file_path_label = tk.Label(box, text="No file/folder selected",
                                       font=("Consolas", 11), bg="#28364a", fg="#70e7d6", wraplength=590, justify="left")
        self.file_path_label.pack(pady=(5, 15))
        recover_btn = tk.Button(box, text="💾 RECOVER FILES",
                               font=("Consolas", 13, "bold"), bg="#194055", fg="#a1ffd9",
                               relief="solid", bd=2, width=20,
                               command=lambda: self.app_logic.recover_file(self.recovery_mode, self.recovery_results))
        recover_btn.pack(pady=10)
        res_label = tk.Label(box, text="RECOVERY RESULTS:",
                             font=("Consolas", 11, "bold"), bg="#28364a", fg="#a1ffd9")
        res_label.pack(pady=(15,3))
        self.recovery_results = scrolledtext.ScrolledText(box, font=("Consolas", 10),
                                                         width=75, height=5,
                                                         bg="#13222F", fg="#a1ffd9")
        self.recovery_results.pack(pady=(2, 14), fill="both", expand=True)

    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def run(self):
        self.setup_main_window()
        self.create_main_page()
        self.app.mainloop()


