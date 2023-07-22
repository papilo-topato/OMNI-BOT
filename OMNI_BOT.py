import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

def main_menu(choice):
    if choice == 1:
        run_calculator()
    elif choice == 2:
        run_weather_app()
    elif choice == 3:
        run_translation()
    elif choice == 4:
        run_flames_app()
    elif choice == 5:
        run_pdfoperations_app()
    elif choice == 6:
        run_texttoimg_app()        
    elif choice == 7:
        exit_app()

def run_calculator():
    subprocess.run(["python", "calculator_app.py"])

def run_weather_app():
    subprocess.run(["python", "weather_app.py"])

def run_translation():
    subprocess.run(["python", "translator_app.py"])

def run_flames_app():
    subprocess.run(["python", "flames_app.py"])

def run_pdfoperations_app():
    subprocess.run(["python", "PDF_Operations_app.py"])
    
def run_texttoimg_app():
    subprocess.run(["python", "text-to-img_generation_app.py"])

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def on_enter(event):
    event.widget.configure(background="#FFC72C")  # Highlighted background color
    event.widget.configure(foreground="white")  # Text color when hovered

def on_leave(event):
    event.widget.configure(background="#3B5F8A")  # Original background color
    event.widget.configure(foreground="black")  # Original text color

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tooltip, text=self.text, background="#FFFFE0", relief=tk.SOLID, borderwidth=1, font=("Arial", 12))
        label.pack(ipadx=5, ipady=2)

    def leave(self, event):
        if self.tooltip:
            self.tooltip.destroy()

root = tk.Tk()
root.title("Omni Bot")

# Stylish fonts
button_style = ttk.Style()
button_style.configure("TButton", font=("Arial", 20))

# Background color for the buttons
button_bg_color = "#4CAF50"  # Green
exit_button_bg_color = "#FF5252"  # Light red

frame = tk.Frame(root, padx=20, pady=20, bg=button_bg_color)
frame.pack()

options = [
    ("Calculator", 1),
    ("Weather App", 2),
    ("Translation", 3),
    ("Flames", 4),
    ("PDF Operations", 5),
    ("Text to Image Generation", 6),
    ("Exit", 7)
]

num_columns = 3

for idx, (option_text, choice) in enumerate(options, 1):
    if option_text == "Translation":
        button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        button.grid(row=1, column=1, padx=10, pady=10, columnspan=1, sticky="ew")
        ToolTip(button, 'Translate text from one language to another')
    elif option_text == "Text to Image Generation":
        button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        button.grid(row=1, column=2, padx=10, pady=10, columnspan=1, sticky="ew")
        ToolTip(button, 'Can generate image from text provided')
    elif option_text == "PDF Operations":
        button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        button.grid(row=1, column=3, padx=10, pady=10, columnspan=1, sticky="ew")
        ToolTip(button, 'Can perform operations on PDF files')    
    elif option_text == "Flames":
        button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        button.grid(row=2, column=1, padx=10, pady=10, columnspan=1, sticky="ew")
        ToolTip(button, 'Can calculate relationship type between two people')
    elif option_text == "Weather App":
        button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        button.grid(row=2, column=2, padx=10, pady=10, columnspan=1, sticky="ew")
        ToolTip(button, 'Can get weather information of a place')
    elif option_text == "Calculator":
        button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        button.grid(row=2, column=3, padx=10, pady=10, columnspan=1, sticky="ew")
        ToolTip(button, 'Can perform basic arithmetic operations')
    elif option_text == "Exit":
        exit_button = ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c), width=18, cursor="hand2")
        exit_button.grid(row=3, column=1, padx=10, pady=10, columnspan=3, sticky="ew")
        ToolTip(exit_button, 'Exit the application')
        button_style.configure("Exit.TButton", background=exit_button_bg_color) 
        button = frame.grid_slaves(row=3, column=1)[0]
        exit_button.configure(style="Exit.TButton")
    else:
        ttk.Button(frame, text=option_text, style="TButton", command=lambda c=choice: main_menu(c)).grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        # Add Enter and Leave events for highlighting and blinking behavior
        button = frame.grid_slaves(row=3, column=1)[0]
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

root.mainloop()
