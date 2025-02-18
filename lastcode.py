import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import time
import mysql.connector
import threading
import cv2  # Importing OpenCV

# Set up GPIO pins for relays and servo
relays = {
    "Apple": 5,
    "Orange": 6,
    "Banana": 13,
    "Grapes": 19,
    "Pineapple": 26
}

servo_pin = 21  # Define the servo pin

GPIO.setmode(GPIO.BCM)
for pin in relays.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

GPIO.setup(servo_pin, GPIO.OUT)

def activate_relay(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(5)
    GPIO.output(pin, GPIO.HIGH)

def control_servo(angle):
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    duty_cycle = angle / 18 + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)
    pwm.stop()

def pca1_action():
    print("PCA1 activated")
    control_servo(90)
    time.sleep(2)

def pca2_action():
    print("PCA2 activated")
    time.sleep(2)

def pca3_action():
    print("PCA3 activated")
    time.sleep(2)

def pca4_action():
    print("PCA4 activated")
    time.sleep(2)

def log_order_to_database(choice):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='lei_mark_cruz',
            password='rasp',
            database='lei_mark_cruz'
        )
        cursor = connection.cursor()
        query = "INSERT INTO orders (choice, quantity) VALUES (%s, %s)"
        cursor.execute(query, (choice, 1))
        connection.commit()
        print(f"{choice} logged to database")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def process_choice(choice):
    pca1_action()
    if messagebox.askokcancel("Confirmation", "Please place the cap. Tap OK when ready."):
        pca2_action()
        activate_relay(relays[choice])
        pca3_action()
        if messagebox.askokcancel("Confirmation", "Please pick up the cup. Tap OK when ready."):
            pca4_action()
            messagebox.showinfo("Thank You", "Thank you for your cooperation!")
            show_ad()
    log_order_to_database(choice)

def confirm_choice(choice):
    if messagebox.askyesno("Confirm", f"Are you sure you want to select {choice}?"):
        for widget in root.winfo_children():
            widget.destroy()
        process_choice(choice)
    else:
        show_ad()

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)  # Open video using OpenCV
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return  # Exit if video cannot be opened
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

    choice1 = tk.Button(choices_canvas, image=choice1_imgtk, command=lambda: confirm_choice("Apple"))
    choice1.image = choice1_imgtk
    choices_canvas.create_window(100, 400, window=choice1)

    choice2 = tk.Button(choices_canvas, image=choice2_imgtk, command=lambda: confirm_choice("Orange"))
    choice2.image = choice2_imgtk
    choices_canvas.create_window(350, 400, window=choice2)

    choice3 = tk.Button(choices_canvas, image=choice3_imgtk, command=lambda: confirm_choice("Banana"))
    choice3.image = choice3_imgtk
    choices_canvas.create_window(600, 400, window=choice3)

    choice4 = tk.Button(choices_canvas, image=choice4_imgtk, command=lambda: confirm_choice("Grapes"))
    choice4.image = choice4_imgtk
    choices_canvas.create_window(850, 400, window=choice4)

    choice5 = tk.Button(choices_canvas, image=choice5_imgtk, command=lambda: confirm_choice("Pineapple"))
    choice5.image = choice5_imgtk
    choices_canvas.create_window(1100, 400, window=choice5)

    # Add labels for each choice
    choices_canvas.create_text(100, 500, text="Apple", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(350, 500, text="Orange", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(600, 500, text="Banana", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(850, 500, text="Grapes", font=('Helvetica', 16), anchor=tk.N)
    choices_canvas.create_text(1100, 500, text="Pineapple", font=('Helvetica', 16), anchor=tk.N)

def show_ad():
    for widget in root.winfo_children():
        widget.destroy()
    video_player = VideoPlayer(root, "ad_video.mp4")
    root.bind("<Button-1>", lambda e: show_choices(video_player))

def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', True)

def end_fullscreen(event=None):
    root.attributes('-fullscreen', False)

root = tk.Tk()
root.title("Advertisement GUI")
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)
root.attributes('-fullscreen', True)
show_ad()
root.mainloop()
