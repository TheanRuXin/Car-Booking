
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\build\assets\frame0\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
from tkinter import Tk, Canvas,Button

window = Tk()

window.geometry("1029x679")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 679,
    width = 1029,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    514.0,
    339.0,
    image=image_image_1
)

button_image_1= PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    command=lambda: button_1(window),
    relief="flat"
)
button_1.place(
    x=177.0,
    y=529.0,
    width=259.0,
    height=90.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,    highlightthickness=0,
    command=lambda:button_2(window),
    relief="flat"
)
button_2.place(
    x=593.30712890625,
    y=529.0,
    width=258.6929016113281,
    height=90.0
)
def button_1(window):
    window.destroy()
    from SignUp import show_SignUp_page
    show_SignUp_page()


def button_2(window):
    window.destroy()
    from LogIn import show_LogIn_page
    show_LogIn_page()

window.resizable(False, False)
window.mainloop()
