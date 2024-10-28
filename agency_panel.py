
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\agency\agency_panel\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def manage_cars(window):
    window.destroy()
    subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\agency\build\manage_car.py"])

def manage_bookings(window):
    window.destroy()

def view_ratings_and_reviews(window):
    window.destroy()

window = Tk()

window.geometry("1221x773")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 773,
    width = 1221,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    610.0,
    386.0,
    image=image_image_1
)

canvas.create_text(
    396.0,
    112.0,
    anchor="nw",
    text="Agency Panel",
    fill="#000000",
    font=("Inter Bold", 64 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:manage_bookings(window),
    relief="flat"
)
button_1.place(
    x=681.0,
    y=265.0,
    width=469.0,
    height=144.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: manage_cars(window),
    relief="flat"
)
button_2.place(
    x=70.0,
    y=265.0,
    width=469.0,
    height=144.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: view_ratings_and_reviews(window),
    relief="flat"
)
button_3.place(
    x=376.0,
    y=502.0,
    width=469.0,
    height=144.0
)
window.resizable(False, False)
window.mainloop()