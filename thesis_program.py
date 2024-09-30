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

def activate_relay(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn on the relay
    time.sleep(5)  # Relay stays on for 5 seconds
    GPIO.output(pin, GPIO.HIGH)  # Turn off the relay

def log_order_to_database(choice):
    """Logs the selected order into the MySQL database"""
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='lei_mark_cruz',
            password='rasp',
            database='lei_mark_cruz'
        )
        cursor = connection.cursor()

        # Insert the selected order into the 'orders' table
        query = "INSERT INTO orders (choice, quantity) VALUES (%s, %s)"
        cursor.execute(query, (choice, 1))  # Set quantity to 1 for each order

        # Commit the transaction to save the data
        connection.commit()

        print(f"{choice} logged to database")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def show_processing(choice):
    # Create a new frame for processing in the front middle
    processing_frame = tk.Frame(root)
    processing_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Add the "Processing..." label
    processing_label = tk.Label(processing_frame, text="Processing...", font=('Helvetica', 24))
    processing_label.pack(pady=10)

    # Add a progress bar
    progress_bar = ttk.Progressbar(processing_frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    root.update_idletasks()

    # Simulate processing with progress bar
    for i in range(100):
        progress_bar['value'] = i + 1
        root.update_idletasks()
        time.sleep(0.05)  # Simulating time delay for progress

    # Activate the relay associated with the choice
    activate_relay(relays[choice])

    # Log the order to the database
    log_order_to_database(choice)

    # Remove processing elements
    processing_label.destroy()
    progress_bar.destroy()

    # Add the "Thank You" message
    thank_you_label = tk.Label(processing_frame, text="Thank You!", font=('Helvetica', 36))
    thank_you_label.pack(pady=20)

    root.update_idletasks()
    time.sleep(3)  # Display "Thank You" for 3 seconds

    # Remove "Thank You" message and frame
    thank_you_label.destroy()
    processing_frame.destroy()

    # Return to advertisement
    show_ad()

def confirm_choice(choice):
    result = messagebox.askyesno("Confirm", f"Are you sure you want to select {choice}?")
    if result:
        for widget in root.winfo_children():
            widget.destroy()
        show_processing(choice)
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
