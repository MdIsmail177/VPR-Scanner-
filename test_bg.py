import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("900x700")

# Use your actual image path below (edit if needed)
image_path = r"C:\Users\MY\Desktop\VPR_Scanner\background.jpg"

try:
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((900, 700), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    print("Background loaded successfully!")
except Exception as e:
    print("Error loading background image:", e)

root.mainloop()