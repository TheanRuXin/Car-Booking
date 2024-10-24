
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import subprocess
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\agency\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def agency_sign_up_page(window):
    window.destroy()
    subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\agency\build\agency_sign_up_page.py"])

def agency_login_page(window):
    window.destroy()
    subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\agency\build\agency_login_page.py"])

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

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: agency_sign_up_page(window),
    relief="flat"
)
button_1.place(
    x=273.0,
    y=536.0,
    width=259.0,
    height=90.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: agency_login_page(window),
    relief="flat"
)
button_2.place(
    x=689.30712890625,
    y=536.0,
    width=258.6929016113281,
    height=90.0
)

canvas.create_text(
    473.0,
    196.0,
    anchor="nw",
    text="AGENCY",
    fill="#000000",
    font=("Inter Bold", 64 * -1)
)
window.resizable(False, False)
window.mainloop()