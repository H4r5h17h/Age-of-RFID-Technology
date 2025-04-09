import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from PIL import Image, ImageTk
from tkinter import Label, Button, Frame
import serial
import threading
import time

# Serial Configuration
PORT = 'COM3'
BAUD_RATE = 9600

# Function to read the RFID value 
def read_rfid():
    try:
        arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allowing connection to stabilize
        while True:
            if arduino.in_waiting > 0:
                hex_value = arduino.readline().decode().strip()
                info_text.set(f"RFID Card UID: {hex_value}")
            time.sleep(0.1)

    # handeling some exceptions
    except serial.SerialException:
        info_text.set("⚠️ Error: RFID Scanner Not Connected")
    except Exception as e:
        info_text.set("⚠️ Error: Unable to Read RFID")


# GUI setup 
#main window
root = tb.Window(themename="default")
root.geometry("500x250")
root.title("Gitam")


# adding gitam logo at the top of the window(top left)
logo_img = Image.open("logo.png")
logo_img = ImageTk.PhotoImage(logo_img)
root.iconphoto(False, logo_img)


# the main heading with frame
header = Frame(root, bg="#006B64",height=45)
header.pack(fill='x')
header_content = Frame(header, bg="#006B64")
header_content.pack(side="top",pady=10)


# adding a logo beside the heading
logo_small = Image.open("logo_white.png").resize((65, 55), Image.LANCZOS) 
logo_small = ImageTk.PhotoImage(logo_small)
Label(header_content,
    image=logo_small, 
    bg="#006B64").pack(side="left", padx=5)
Label(header_content, 
    text="Gitam RFID Scanner", 
    font=("Arial", 16, "bold"), 
    fg="white", bg="#006B64").pack(side="left", padx=5)



# RFID Status Label
info_text = tk.StringVar(value="Waiting for RFID Card...")
info_label = tk.Label(root, 
    textvariable=info_text, 
    font=("Arial", 14), bg="white", 
    padx=10, pady=10, 
    relief="ridge", bd=2)
info_label.pack(pady=30)

# Start RFID Reader Thread
# This will work in the background once after main program is started
threading.Thread(target=read_rfid, daemon=True).start()

root.mainloop()
