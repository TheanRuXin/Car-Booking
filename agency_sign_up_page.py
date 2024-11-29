import sys
from pathlib import Path
import sqlite3
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,messagebox
import subprocess
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\agency\build\assets\frame3")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def back():
    window.destroy()
    subprocess.Popen([sys.executable,r"C:\Users\User\Documents\Ruxin file\build\agency\build\agency_first_page.py"])

#Database setup
conn = sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")
c = conn.cursor()

# Create a table for users
c.execute('''CREATE TABLE IF NOT EXISTS Agency_details
            (agency_id INTEGER PRIMARY KEY AUTOINCREMENT, agency_name TEXT, agency_phone_number TEXT, agency_email TEXT, agency_password TEXT)''')
conn.commit()
conn.close()

#Function to register a new user
def agency_sign_up():
    conn = sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")
    c = conn.cursor()

    agency_name = entry_1.get().strip()
    agency_phone_number = entry_2.get().strip()
    agency_email = entry_3.get().strip()
    agency_password = entry_4.get().strip()
    confirm_password = entry_5.get().strip()

    #validate input
    if not agency_name or not agency_phone_number or not agency_email or not agency_password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!")
        conn.close()
        return
    if len(agency_password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long!")
        conn.close()
        return
    if agency_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        conn.close()
        return

    c.execute("SELECT * FROM Agency_details WHERE agency_email = ? AND agency_password = ?", (agency_email,agency_password))
    existing_user = c.fetchone()

    agency_email = entry_3.get().strip()
    agency_password = entry_4.get().strip()

    # Validate input
    if existing_user:
        messagebox.showerror("Error", "Email and Password are required!")
        window.destroy()
        subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\agency\build\agency_first_page.py"])
        conn.close()
        return

    c.execute("Insert INTO Agency_details (agency_name, agency_phone_number, agency_email, agency_password) VALUES(?, ?, ?, ?)",(agency_name, agency_phone_number, agency_email, agency_password))
    conn.commit()
    messagebox.showinfo("Success","Sign Up successful! Please Log in.")
    window.destroy()
    subprocess.Popen([sys.executable,r"C:\Users\User\Documents\Ruxin file\build\agency\build\agency_login_page.py"])

    conn.close()

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
    612.0,
    386.0,
    image=image_image_1
)

Button(window, text="Back", command=lambda:back(), font=("Arial", 20),bg="black",fg="white").place(x=700.0, y=672.0, width=150.0,height=40.0)
Button(window, text="Sign Up", command=lambda:agency_sign_up(), font=("Arial", 20),bg="yellow",fg="black").place(x=350.0, y=672.0, width=150.0, height=40.0)
canvas.create_text(
    258.0,
    123.0,
    anchor="nw",
    text="Name:",
    fill="#000000",
    font=("Inter Bold", 40 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    608.5,
    195.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1)
)
entry_1.place(
    x=249.0,
    y=171.0,
    width=719.0,
    height=46.0
)

canvas.create_text(
    253.0,
    228.0,
    anchor="nw",
    text="Phone Number:",
    fill="#000000",
    font=("Inter Bold", 40 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    608.5,
    304.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1)
)
entry_2.place(
    x=249.0,
    y=281.0,
    width=719.0,
    height=45.0
)

canvas.create_text(
    253.0,
    339.0,
    anchor="nw",
    text="Email:",
    fill="#000000",
    font=("Inter Bold", 40 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    612.5,
    413.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1)
)
entry_3.place(
    x=253.0,
    y=389.0,
    width=719.0,
    height=46.0
)

canvas.create_text(
    256.0,
    453.0,
    anchor="nw",
    text="Password:",
    fill="#000000",
    font=("Inter Bold", 40 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    612.5,
    525.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1),show="*"
)
entry_4.place(
    x=253.0,
    y=501.0,
    width=719.0,
    height=46.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    612.5,
    631.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,font=("Inter Bold", 40 * -1),show="*"
)
entry_5.place(
    x=253.0,
    y=607.0,
    width=719.0,
    height=46.0
)

canvas.create_text(
    253.0,
    560.0,
    anchor="nw",
    text="Comfirm Password:",
    fill="#000000",
    font=("Inter Bold", 40 * -1)
)

canvas.create_text(
    488.0,
    57.0,
    anchor="nw",
    text="Sign Up",
    fill="#000000",
    font=("Inter Bold", 55 * -1)
)
window.resizable(False, False)
window.mainloop()
