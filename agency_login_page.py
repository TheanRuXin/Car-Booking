import sys
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
import sqlite3
from tkinter import Tk, Canvas, Entry, Text, Button, messagebox, PhotoImage
import subprocess,sys


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\agency\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def agency_login():
    conn = sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")
    c = conn.cursor()

    agency_ID = entry_1.get().strip()
    agency_password = entry_2.get().strip()

    # Validate input
    if not agency_ID or not agency_password:
        messagebox.showerror("Error", "ID and Password are required!")
        conn.close()
        return

    c.execute("SELECT * FROM Agency_details WHERE agency_ID = ? AND agency_password = ?", (agency_ID, agency_password))
    result = c.fetchone()

    if result:
        messagebox.showinfo("Success", "LogIn successful!")
        window.withdraw()
        subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\agency\agency_panel\build\agency_panel.py"])

    else:
        messagebox.showerror("Error", "Invalid ID or password!")


    conn.close()

def back():
    window.destroy()
    subprocess.Popen([sys.executable,r"C:\Users\User\Documents\Ruxin file\build\agency\build\agency_first_page.py"])

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
    333.0,
    263.0,
    anchor="nw",
    text="ID:",
    fill="#000000",
    font=("Inter Bold", 48 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    610.5,
    344.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1)
)
entry_1.place(
    x=333.0,
    y=320.0,
    width=555.0,
    height=46.0
)

canvas.create_text(
    333.0,
    394.0,
    anchor="nw",
    text="Password:",
    fill="#000000",
    font=("Inter Bold", 48 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    610.5,
    469.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1),show="*"
)
entry_2.place(
    x=333.0,
    y=445.0,
    width=555.0,
    height=46.0
)

canvas.create_text(
    447.0,
    131.0,
    anchor="nw",
    text="Log in",
    fill="#000000",
    font=("Inter Bold", 60 * -1)
)
Button(window, text="Back", command=lambda:back(), font=("Arial", 20),bg="black",fg="white").place(x=700.0, y=600.0, width=150.0,height=40.0)
Button(window, text="Log In", command=lambda:agency_login(), font=("Arial", 20),bg="yellow",fg="black").place(x=350.0, y=600.0, width=150.0, height=40.0)
window.resizable(False, False)
window.mainloop()
