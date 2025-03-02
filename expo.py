import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import time
import cv2
import mysql.connector

# Set up GPIO pins for relays
relays = {
    "Apple": 5,
    "Orange": 6,
    "Banana": 13,
    "Grapes": 19,
    "Pineapple": 26
}

GPIO.setmode(GPIO.BCM)
for pin in relays.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Global variable to track inactivity timeout
timeout_id = None

def reset_to_ad():
    """Resets the program back to advertisement after 30 seconds of inactivity."""
    global timeout_id
    timeout_id = None
    show_ad()  # Restart the advertisement

def restart_timer():
    """Resets the inactivity timer whenever the screen is touched."""
    global timeout_id
    if timeout_id is not None:
        root.after_cancel(timeout_id)  # Cancel the previous timer
    timeout_id = root.after(30000, reset_to_ad)  # Start a new 30-second timer

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.label = ttk.Label(root)
        self.label.pack(fill=tk.BOTH, expand=True)
        self.video_playing = True
        self.play_video()

    def play_video(self):
        if self.video_playing:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
                self.root.after(10, self.play_video)

    def stop_video(self):
        self.video_playing = False
        self.cap.release()

def show_choices(video_player):
    restart_timer()  # Restart inactivity timer on touch
    video_player.stop_video()
    video_player.label.pack_forget()

    choices_canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    choices_canvas.pack(fill=tk.BOTH, expand=True)

    bg_image = Image.open("background.png")
    bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    choices_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)
    choices_canvas.image = bg_image_tk

    choices = [
        ("Apple", "choice1.png", 100),
        ("Orange", "choice2.png", 350),
        ("Banana", "choice3.png", 600),
        ("Grapes", "choice4.png", 850),
        ("Pineapple", "choice5.png", 1100),
    ]

    for name, img_path, x in choices:
        img = Image.open(img_path).resize((150, 150), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(img)
        btn = tk.Button(choices_canvas, image=imgtk, command=lambda n=name: confirm_choice(n))
        btn.image = imgtk
        choices_canvas.create_window(x, 400, window=btn)
        choices_canvas.create_text(x, 500, text=name, font=('Helvetica', 16), anchor=tk.N)

def show_ad():
    for widget in root.winfo_children():
        widget.destroy()
    video_player = VideoPlayer(root, "ad_video.mp4")
    root.bind("<Button-1>", lambda e: [restart_timer(), show_choices(video_player)])

def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', True)

def end_fullscreen(event=None):
    root.attributes('-fullscreen', False)

# Create the main window
root = tk.Tk()
root.title("Advertisement GUI")

# Bind F11 to toggle fullscreen
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)

# Start in fullscreen mode
root.attributes('-fullscreen', True)

# Show the initial advertisement
show_ad()

# Start the inactivity timer
restart_timer()

# Run the GUI loop
root.mainloop()
