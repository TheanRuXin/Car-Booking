
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import sqlite3
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,messagebox
from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\adminpage\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


#Database setup
conn = sqlite3.connect('Users.db')
c = conn.cursor()

# Create a table for users
c.execute('''CREATE TABLE IF NOT EXISTS Users
            (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, phone_number TEXT, email TEXT, password TEXT)''')
conn.commit()
conn.close()

#Function to register a new user
def SignUp_user(window):
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()

    username = entry_1.get().strip()
    phone_number = entry_2.get().strip()
    email = entry_3.get().strip()
    password = entry_4.get().strip()
    confirm_password = entry_5.get().strip()

    #validate input
    if not username or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!")
        conn.close()
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        conn.close()
        return

    c.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email,password))
    existing_user = c.fetchone()

    email = entry_3.get().strip()
    password = entry_4.get().strip()

    # Validate input
    if existing_user:
        messagebox.showerror("Error", "Email and Password are required!")
        window.destroy()
        from FristPage import show_first_page
        show_first_page()
        conn.close()
        return

    c.execute("Insert INTO Users (username, phone_number, email, password) VALUES(?, ?, ?, ?)",(username, phone_number, email, password))
    conn.commit()
    messagebox.showinfo("Success","Sign Up successful! Please Log in.")
    window.destroy()
    from LogIn import show_logIn_page
    show_logIn_page()

    conn.close()

#Registration Page
def show_SignUp_page():
    global entry_1,entry_2,entry_3,entry_4,entry_5

    window = Tk()
    window.geometry("1029x679")
    window.configure(bg = "#FFFFFF")

    canvas = Canvas(window,bg = "#FFFFFF",height = 679,width = 1029,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(514.0, 339.0,image=image_image_1)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=lambda: SignUp_user(window) ,relief="flat")
    button_1.place(x=441.0,y=624.0,width=147.0,height=45.0)

    canvas.create_text(157.0,75.0,anchor="nw",text="Username:",fill="#000000",font=("Inter Bold", 40 * -1))
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_1 = canvas.create_image(512.5,147.0,image=entry_image_1)

    entry_1 = Entry(bd=3,bg="#FFFFFF",fg="#000716",highlightthickness=0,font=("Inter Bold",40 * -1))
    entry_1.place(x=153.0,y=123.0,width=719.0,height=46.0)
    canvas.create_text(157.0,180.0,anchor="nw",text="Phone Number:",fill="#000000",font=("Inter Bold", 40 * -1))
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_2 = canvas.create_image(512.5,256.5,image=entry_image_2)

    entry_2 = Entry(bd=3,bg="#FFFFFF",fg="#000716",highlightthickness=0,font=("Inter Bold",40 * -1))
    entry_2.place(x=153.0,y=233.0,width=719.0,height=45.0)
    canvas.create_text(157.0,291.0,anchor="nw",text="Email:",fill="#000000",font=("Inter Bold", 40 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(516.5,365.0,image=entry_image_3)
    entry_3 = Entry(bd=3,bg="#FFFFFF",fg="#000716",highlightthickness=0,font=("Inter Bold",40 * -1))
    entry_3.place(x=157.0,y=341.0,width=719.0,height=46.0)

    canvas.create_text(160.0,405.0,anchor="nw",text="Password:",fill="#000000",font=("Inter Bold", 40 * -1))
    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(516.5,477.0,image=entry_image_4)
    entry_4 = Entry(bd=3,bg="#FFFFFF",fg="#000716",highlightthickness=0,show="*",font=("Inter Bold",40 * -1))
    entry_4.place(x=157.0,y=453.0, width=719.0,height=46.0)

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(516.5,583.0,image=entry_image_5)
    entry_5 = Entry(bd=3,bg="#FFFFFF",fg="#000716",highlightthickness=0,show="*" ,font=("Inter Bold",40 * -1))
    entry_5.place(x=157.0,y=559.0,width=719.0,height=46.0)
    canvas.create_text(157.0,512.0,anchor="nw",text="Confirm Password:",fill="#000000",font=("Inter Bold", 40 * -1))
    canvas.create_text(392.0,9.0,anchor="nw",text="Sign Up",fill="#000000",font=("Inter Bold", 55 * -1))

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    show_SignUp_page()


