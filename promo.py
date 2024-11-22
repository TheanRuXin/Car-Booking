
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,messagebox
from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk
import sqlite3, os,sys,subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def connect_db():
    return sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")

def cars_button(user_id):
    window.withdraw()
    subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\car.py",str(user_id)])

def profile_button(user_id):
    window.withdraw()
    subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\profile.py",str(user_id)])

def get_latest_promotion():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, description, discount_percentage, start_date, end_date, promo_code, image_path
        FROM promotions
        ORDER BY promotion_id DESC LIMIT 1
    ''')
    promotion = cursor.fetchone()
    conn.close()
    return promotion

def display_promo():
    # Fetch promotion details
    promotion = get_latest_promotion()
    if not promotion:
        # Handle case where no promotion is found
        promotion_name = "No promotion available"
        promotion_description = ""
        promotion_discount = ""
        promotion_start_date = ""
        promotion_end_date = ""
        promotion_promo_code = ""
        promotion_image_path = ""
    else:
        promotion_name, promotion_description, promotion_discount, promotion_start_date, promotion_end_date, promotion_promo_code, promotion_image_path = promotion


    global window
    window = Tk()
    window.geometry("1221x773")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=773,
        width=1221,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    x_position = 600
    canvas.create_rectangle(63.0, 215.0, 1150.0, 520.0, fill="grey", outline="grey", width=1)
    canvas.create_text(x_position, 260, text=promotion_name, font=("Comic Sans MS", 22),anchor="w",fill="white")
    canvas.create_text(x_position, 300, text=promotion_description, font=("Comic Sans MS", 16),anchor="w",fill="white")
    canvas.create_text(x_position, 340, text=f"Discount: {promotion_discount}%", font=("Comic Sans MS", 16),anchor="w",fill="white")
    canvas.create_text(x_position, 380, text=f"Start Date: {promotion_start_date}", font=("Comic Sans MS", 14),anchor="w",fill="white")
    canvas.create_text(x_position, 420, text=f"End Date: {promotion_end_date}", font=("Comic Sans MS", 14),anchor="w",fill="white")
    canvas.create_text(x_position, 460, text=f"Promo Code: {promotion_promo_code}", font=("Comic Sans MS", 14), anchor="w",fill="white")

    # Display promotion image (if available)
    if promotion_image_path and os.path.isfile(promotion_image_path):
        img = Image.open(promotion_image_path)
        img = img.resize((450, 250), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        image_label = Label(window, image=tk_img)
        image_label.image = tk_img
        image_label.place(x=83, y=240)
    else:
        Label(window, text="No Image Available", font=("Arial", 12)).pack(pady=10)

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        63.0,
        152.0,
        anchor="nw",
        text="Promo",
        fill="#000000",
        font=("KaiseiDecol Medium", 40 * -1)
    )

    canvas.create_text(
        63.0,
        541.0,
        anchor="nw",
        text="Contact",
        fill="#000000",
        font=("KaiseiDecol Medium", 40 * -1)
    )

    canvas.create_text(
        141.0,
        627.0,
        anchor="nw",
        text="017-789 1011",
        fill="#000000",
        font=("KaiseiDecol Medium", 32 * -1)
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        1221.0,
        113.0,
        fill="#DFDFDF",
        outline="")

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        86.0,
        57.0,
        image=image_image_2
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: profile_button(user_id),
        relief="flat"
    )
    button_1.place(
        x=1126.0,
        y=31.0,
        width=49.0,
        height=49.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(
        x=1010.0,
        y=30.0,
        width=90.0,
        height=52.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cars_button(user_id),
        relief="flat"
    )
    button_5.place(
        x=917.0,
        y=30.0,
        width=70.0,
        height=52.0
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        85.0,
        642.0,
        image=image_image_3
    )
    if len(sys.argv) < 2:
        messagebox.showerror("Error", "User ID not provided.")
        sys.exit(1)

    user_id = int(sys.argv[1])
    window.resizable(False, False)
    window.mainloop()
display_promo()
