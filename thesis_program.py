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

    choices_canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    choices_canvas.pack(fill=tk.BOTH, expand=True)

    # Load background image
    bg_image = Image.open("background.png")
    bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    choices_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)
    choices_canvas.image = bg_image_tk  # Keep a reference to avoid garbage collection

    # Load and resize images for buttons
    choice1_img = Image.open("choice1.png").resize((150, 150), Image.LANCZOS)
    choice2_img = Image.open("choice2.png").resize((150, 150), Image.LANCZOS)
    choice3_img = Image.open("choice3.png").resize((150, 150), Image.LANCZOS)
    choice4_img = Image.open("choice4.png").resize((150, 150), Image.LANCZOS)
    choice5_img = Image.open("choice5.png").resize((150, 150), Image.LANCZOS)

    choice1_imgtk = ImageTk.PhotoImage(choice1_img)
    choice2_imgtk = ImageTk.PhotoImage(choice2_img)
    choice3_imgtk = ImageTk.PhotoImage(choice3_img)
    choice4_imgtk = ImageTk.PhotoImage(choice4_img)
    choice5_imgtk = ImageTk.PhotoImage(choice5_img)

    choice1 = tk.Button(choices_canvas, image=choice1_imgtk, command=lambda: choice_selected("Choice 1"))
    choice1.image = choice1_imgtk
    choices_canvas.create_window(100, 400, window=choice1)

    choice2 = tk.Button(choices_canvas, image=choice2_imgtk, command=lambda: choice_selected("Choice 2"))
    choice2.image = choice2_imgtk
    choices_canvas.create_window(350, 400, window=choice2)

    choice3 = tk.Button(choices_canvas, image=choice3_imgtk, command=lambda: choice_selected("Choice 3"))
    choice3.image = choice3_imgtk
    choices_canvas.create_window(600, 400, window=choice3)

    choice4 = tk.Button(choices_canvas, image=choice4_imgtk, command=lambda: choice_selected("Choice 4"))
    choice4.image = choice4_imgtk
    choices_canvas.create_window(850, 400, window=choice4)

    choice5 = tk.Button(choices_canvas, image=choice5_imgtk, command=lambda: choice_selected("Choice 5"))
    choice5.image = choice5_imgtk
    choices_canvas.create_window(1100, 400, window=choice5)

    # Add labels for each choice
    choices_canvas.create_text(100, 500, text="Apple", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(350, 500, text="Orange", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(600, 500, text="Banana", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(850, 500, text="Grapes", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(1100, 500, text="Pineapple", font=('Helvetica', 16), anchor=tk.N)

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
