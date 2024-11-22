

# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess, sys


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def sign_up_button(window):
    window.withdraw()
    subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\sign_up.py"])

def log_in_button(window):
    window.withdraw()
    subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\log_in.py"])

def show_first_page():
    window = Tk()

    window.geometry("1221x773")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=773, width=1221, bd=0, highlightthickness=0, relief="ridge")

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(610.0, 386.0, image=image_image_1)

    canvas.create_text(67.0, 215.0, anchor="nw", text="Adventure with ", fill="#FFFFFF",font=("Rakkas Regular", 64 * -1))

    canvas.create_text(67.0, 279.0, anchor="nw", text="Ease!", fill="#FFFFFF", font=("Rakkas Regular", 64 * -1))

    canvas.create_text(67.0, 151.0, anchor="nw", text="Drive Your", fill="#FFFFFF", font=("Rakkas Regular", 64 * -1))

    canvas.create_text(37.0, 25.0, anchor="nw", text="CarRental", fill="#09CED5", font=("Kanit Bold", 36 * -1))

    canvas.create_text(67.0, 366.0, anchor="nw", text="From city drives to road trips, our ", fill="#FFFFFF",
                       font=("Average Regular", 30 * -1))

    canvas.create_text(68.0, 396.0, anchor="nw", text="fleet is ready to take you wherever", fill="#FFFFFF",
                       font=("Average Regular", 30 * -1))

    canvas.create_text(67.0, 426.0, anchor="nw", text="you need to go.", fill="#FFFFFF",font=("Average Regular", 30 * -1))

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0,command=lambda: sign_up_button(window), relief="flat")
    button_4.place(x=923.0, y=38.0, width=97.0, height=52.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0,command=lambda: log_in_button(window), relief="flat")
    button_5.place(x=1044.0, y=38.0, width=97.0, height=52.0)
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    show_first_page()
