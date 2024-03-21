import tkinter as tk
from tkinter import ttk, filedialog
import pyttsx3
import threading
import time
import PyPDF2

def read_text():
    global paused
    if paused:
        paused = False
        read_button.config(state=tk.DISABLED)  # Disable the "Read Aloud" button
        pause_button.config(state=tk.NORMAL)  # Enable the "Pause" button
        pitch_scale.config(state=tk.DISABLED)  # Disable pitch slider
        speed_scale.config(state=tk.DISABLED)  # Disable speed slider
        words_per_chunk_scale.config(state=tk.DISABLED)  # Disable words per chunk slider
        pause_duration_scale.config(state=tk.DISABLED)  # Disable pause duration slider
        thread = threading.Thread(target=read_aloud, args=(get_text_to_read(), words_per_chunk_scale.get(), pause_duration_scale.get(), current_position))
        thread.start()
    else:
        # Disable sliders during reading
        pitch_scale.config(state=tk.DISABLED)  # Disable pitch slider
        speed_scale.config(state=tk.DISABLED)  # Disable speed slider
        words_per_chunk_scale.config(state=tk.DISABLED)  # Disable words per chunk slider
        pause_duration_scale.config(state=tk.DISABLED)  # Disable pause duration slider
        
        read_button.config(state=tk.DISABLED)  # Disable the "Read Aloud" button
        pause_button.config(state=tk.NORMAL)  # Enable the "Pause" button
        thread = threading.Thread(target=read_aloud, args=(get_text_to_read(), words_per_chunk_scale.get(), pause_duration_scale.get(), 0))
        thread.start()

def get_text_to_read():
    if file_path.get():
        if file_path.get().endswith('.pdf'):
            return extract_text_from_pdf(file_path.get())
        else:
            return read_text_from_file(file_path.get())
    else:
        return text_entry.get("1.0", tk.END)

def read_aloud(text, words_per_chunk, pause_duration, start_position):
    global paused, current_position
    engine.setProperty('rate', speed_scale.get())  # Set speech rate
    engine.setProperty('pitch', pitch_scale.get())  # Set speech pitch
    words = text.split()
    current_position = start_position
    for i in range(start_position, len(words), words_per_chunk):
        if paused:
            break
        chunk = ' '.join(words[i:i+words_per_chunk])
        engine.say(chunk)
        engine.runAndWait()
        current_position = i + words_per_chunk
        time.sleep(pause_duration)
    
    # Enable sliders after reading
    pitch_scale.config(state=tk.NORMAL)  # Enable pitch slider
    speed_scale.config(state=tk.NORMAL)  # Enable speed slider
    words_per_chunk_scale.config(state=tk.NORMAL)  # Enable words per chunk slider
    pause_duration_scale.config(state=tk.NORMAL)  # Enable pause duration slider
    read_button.config(state=tk.NORMAL)  # Enable the "Read Aloud" button
    pause_button.config(state=tk.DISABLED)  # Disable the "Pause" button

# This will extract the text from pdf -> Isn't perfectly functional
def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# What happens when i pause or resume is controlled here
def pause_resume():
    global paused
    paused = not paused
    if paused:
        pause_button.config(state=tk.DISABLED)  # Disable the "Pause" button
        read_button.config(state=tk.NORMAL)  # Enable the "Read Aloud" button
        pitch_scale.config(state=tk.NORMAL)  # Enable pitch slider
        speed_scale.config(state=tk.NORMAL)  # Enable speed slider
        words_per_chunk_scale.config(state=tk.NORMAL)  # Enable words per chunk slider
        pause_duration_scale.config(state=tk.NORMAL)  # Enable pause duration slider
    else:
        pause_button.config(state=tk.NORMAL)  # Enable the "Pause" button
        read_button.config(state=tk.DISABLED)  # Disable the "Read Aloud" button
        pitch_scale.config(state=tk.DISABLED)  # Disable pitch slider
        speed_scale.config(state=tk.DISABLED)  # Disable speed slider
        words_per_chunk_scale.config(state=tk.DISABLED)  # Disable words per chunk slider
        pause_duration_scale.config(state=tk.DISABLED)  # Disable pause duration slider


def toggle_theme():
    global text_color
    if root["bg"] == "#ffffff":
        # Switch to dark theme
        root["bg"] = "#212121"
        text_color = "#ffffff"
        text_label["bg"] = "#212121"
        text_label["fg"] = "#ffffff"
        text_entry["bg"] = "#424242"
        read_button["bg"] = "#757575"
        read_button["fg"] = "#ffffff"
        pause_button["bg"] = "#757575"
        pause_button["fg"] = "#000000"
        pitch_scale["bg"] = "#212121"
        pitch_scale["fg"] = "#ffffff"  
        speed_scale["bg"] = "#212121"
        speed_scale["fg"] = "#ffffff"  
        words_per_chunk_scale["bg"] = "#212121"
        words_per_chunk_scale["fg"] = "#ffffff"  
        pause_duration_scale["bg"] = "#212121"
        pause_duration_scale["fg"] = "#ffffff"  
    else:
        # Switch to light theme
        root["bg"] = "#ffffff"
        text_color = "#000000"
        text_label["bg"] = "#ffffff"
        text_label["fg"] = "#000000"
        text_entry["bg"] = "#f0f0f0"
        read_button["bg"] = "#4682b4"
        read_button["fg"] = "#ffffff"
        pause_button["bg"] = "#4682b4"
        pause_button["fg"] = "#ffffff"
        pitch_scale["bg"] = "#ffffff"
        pitch_scale["fg"] = "#000000"  
        speed_scale["bg"] = "#ffffff"
        speed_scale["fg"] = "#000000"  
        words_per_chunk_scale["bg"] = "#ffffff"
        words_per_chunk_scale["fg"] = "#000000"  
        pause_duration_scale["bg"] = "#ffffff"
        pause_duration_scale["fg"] = "#000000"  

# primary color
text_color = "#000000"

def browse_file():
    file_path.set(filedialog.askopenfilename())

# Initialize tkinter
root = tk.Tk()
root.title("Assignment Helper")

# Set background color
root.config(bg="#ffffff")

# Add custom font
custom_font = ("Helvetica", 12)

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the size of the window
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

# label for text entry
text_label = tk.Label(root, text="Paste your text here:", font=custom_font, bg="#ffffff")
text_label.pack()

# text area
text_entry = tk.Text(root, height=10, width=50, bg="#f0f0f0", font=custom_font, padx=10, pady=10)
text_entry.pack()

# buttons
read_button = tk.Button(root, text="Read Aloud", command=read_text, bg="#4682b4", fg="#ffffff", font=custom_font, padx=10, pady=5, cursor="hand2")
read_button.pack(pady=(0, 10))

pause_button = tk.Button(root, text="Pause", command=pause_resume, bg="#4682b4", fg="#ffffff", font=custom_font, padx=10, pady=5, cursor="hand2")
pause_button.pack(pady=(0, 10))

pause_button.config(state=tk.DISABLED)  # Disable the "Pause" button initially

# sliders for adjusting pitch and speed
pitch_scale = tk.Scale(root, from_=0.5, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Pitch", bg="#ffffff", font=custom_font, length=window_width - 40, cursor="hand2", troughcolor="#4682b4", highlightthickness=0, sliderlength=20, sliderrelief="flat")
pitch_scale.config(troughcolor="#4682b4", sliderlength=20, sliderrelief="flat")
pitch_scale.pack()

speed_scale = tk.Scale(root, from_=100, to=200, orient=tk.HORIZONTAL, label="Speed", bg="#ffffff", font=custom_font, length=window_width - 40, cursor="hand2", troughcolor="#4682b4", highlightthickness=0, sliderlength=20, sliderrelief="flat")
speed_scale.config(troughcolor="#4682b4", sliderlength=20, sliderrelief="flat")
speed_scale.set(100)  # Set default speed to 100
speed_scale.pack()

words_per_chunk_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="Words per Chunk", bg="#ffffff", font=custom_font, length=window_width - 40, cursor="hand2", troughcolor="#4682b4", highlightthickness=0, sliderlength=20, sliderrelief="flat")
words_per_chunk_scale.config(troughcolor="#4682b4", sliderlength=20, sliderrelief="flat")
words_per_chunk_scale.set(4)  # Set default words per chunk to 4
words_per_chunk_scale.pack()

pause_duration_scale = tk.Scale(root, from_=0.3, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Pause Duration (s)", bg="#ffffff", font=custom_font, length=window_width - 40, cursor="hand2", troughcolor="#4682b4", highlightthickness=0, sliderlength=20, sliderrelief="flat")
pause_duration_scale.config(troughcolor="#4682b4", sliderlength=20, sliderrelief="flat")
pause_duration_scale.set(1)  # Set default pause duration to 1 second
pause_duration_scale.pack()

# Button to browse and select a file
browse_button = tk.Button(root, text="Browse File", command=browse_file, bg="#4682b4", fg="#ffffff", font=custom_font, padx=10, pady=5, cursor="hand2")
browse_button.pack(pady=(10, 0))

# Variable to store the selected file path
file_path = tk.StringVar()

# button to toggle between light and dark themes
theme_button = tk.Button(root, text="Dark Mode", command=toggle_theme, bg="#4682b4", fg="#ffffff", font=custom_font, padx=10, pady=5, cursor="hand2")
theme_button.place(x=10, y=10)  # Position the button in the top-left corner

# Made by captain -> footer 
footer_label = tk.Label(root, text="Made by Captain", font=custom_font, bg=root["bg"], fg=text_color)
footer_label.pack(side="bottom", pady=10)

# Initialize pyttsx3 engine
engine = pyttsx3.init()
paused = False
current_position = 0

root.mainloop()
