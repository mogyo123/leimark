import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import time
from playsound import playsound
import cv2
import mysql.connector
import threading
from adafruit_servokit import ServoKit

# Set up GPIO pins for relays
relays = {
    "Water": 5,
    "Redwine": 6,
    "Wine": 13,
    "Pineapple": 19,
    "Orange": 26
}

kit = ServoKit(channels=16)
servo_channel = 5  # Change this to your servo channel
servo_channel_1 = 6
servo_channel_2 = 7
servo_channel_3 = 8
servo_channel_4 = 0
servo_channel_5 = 1
servo_channel_6 = 2
servo_channel_7 = 3
servo_channel_8 = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in relays.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def activate_relay(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2)
    GPIO.output(pin, GPIO.HIGH)
    print("Relay on")

def play_sound(file):
    threading.Thread(target=playsound, args=(file,), daemon=True).start()

def smooth_move(servo, start, end, step=1, delay=0.05):
    """Move servo smoothly from start to end with controlled speed."""
    if start < end:
        for angle in range(start, end + 1, step):
            servo.angle = angle
            time.sleep(delay)
    else:
        for angle in range(start, end - 1, -step):
            servo.angle = angle
            time.sleep(delay)

def pca1_action():
    print("PCA1 activated")
    smooth_move(kit.servo[servo_channel], 180, 130, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_4], 0, 100, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_1], 180, 50, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_2], 0, 110, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel], 130, 80, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_5], 0, 60, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_2], 110, 70, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_4], 100, 65, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_6], 0, 85, step=1, delay=00.01)
    play_sound("1.mp3")
    time.sleep(1)
def pca2_action():
    print("PCA2 activated")
  #  smooth_move(kit.servo[servo_channel_4], 80, 70, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_2], 70, 110, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel], 80, 130, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_3], 0, 130, step=1, delay=00.01)
    time.sleep(1)

def pca3_action():
    print("PCA3 activated")
    time.sleep(3)
    smooth_move(kit.servo[servo_channel_3], 130, 0, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel], 130, 80, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_2], 110, 45, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_4], 65, 100, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_8], 100, 50, step=1, delay=00.01)
    play_sound("2.mp3")
    time.sleep(2)

def pca4_action():
    print("PCA4 activated")
   # smooth_move(kit.servo[servo_channel], 90, 0, step=1, delay=0.1)
    smooth_move(kit.servo[servo_channel_8], 50, 100, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_5], 60, 0, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_2], 45, 110, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_1], 50, 180, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_2], 110, 0, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel], 80, 180, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_6], 85, 0, step=1, delay=00.01)
    smooth_move(kit.servo[servo_channel_4], 100, 0, step=1, delay=00.01)
    play_sound("3.mp3")
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
    video_player.stop_video()
    video_player.label.pack_forget()
    
    choices_canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    choices_canvas.pack(fill=tk.BOTH, expand=True)
    
    bg_image = Image.open("background.png").resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    choices_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)
    choices_canvas.image = bg_image_tk  
    
    choice_images = [Image.open(f"choice{i+1}.png").resize((150, 150), Image.LANCZOS) for i in range(5)]
    choice_imgtk_list = [ImageTk.PhotoImage(img) for img in choice_images]
    
    button_width, button_spacing = 170, 2
    total_width = (button_width * 5) + (button_spacing * 4)
    start_x = (root.winfo_width() - total_width) // 2
    
    fruit_names = ["Water", "Wine", "Redwine", "Pineapple", "Orange"]
    
    for i, (imgtk, fruit_name) in enumerate(zip(choice_imgtk_list, fruit_names)):
        choice_button = tk.Button(choices_canvas, image=imgtk, command=lambda fruit=fruit_name: confirm_choice(fruit))
        choice_button.image = imgtk
        choices_canvas.create_window(start_x + i * (button_width + button_spacing), 300, window=choice_button)
        choices_canvas.create_text(start_x + i * (button_width + button_spacing), 380, text=fruit_name, font=('Georgia', 16), anchor=tk.N)

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

