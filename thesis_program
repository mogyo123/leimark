import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2


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
                # Resize frame to fit the screen
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
    video_player.stop_video()
    video_player.label.pack_forget()

    choices_frame = tk.Frame(root)
    choices_frame.pack(fill=tk.BOTH, expand=True)

    choice1 = tk.Button(choices_frame, text="emman", width=20, height=2, command=lambda: choice_selected("Choice 1"))
    choice1.pack(pady=10)

    choice2 = tk.Button(choices_frame, text="makoy", width=20, height=2, command=lambda: choice_selected("Choice 2"))
    choice2.pack(pady=10)

    choice3 = tk.Button(choices_frame, text="lei", width=20, height=2, command=lambda: choice_selected("Choice 3"))
    choice3.pack(pady=10)

    choice4 = tk.Button(choices_frame, text="troy", width=20, height=2, command=lambda: choice_selected("Choice 4"))
    choice4.pack(pady=10)

    choice5 = tk.Button(choices_frame, text="rico", width=20, height=2, command=lambda: choice_selected("Choice 5"))
    choice5.pack(pady=10)

def choice_selected(choice):
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text=f"You selected {choice}", font=('Helvetica', 16))
    label.pack(pady=20)

    back_button = tk.Button(root, text="Back to Ad", width=20, height=2, command=show_ad)
    back_button.pack(pady=10)

def show_ad():
    for widget in root.winfo_children():
        widget.destroy()

    video_player = VideoPlayer(root, "ad_video.mp4")

    root.bind("<Button-1>", lambda e: show_choices(video_player))

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

# Run the GUI loop
root.mainloop()

