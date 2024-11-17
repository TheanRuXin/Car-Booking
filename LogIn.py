
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\assets\frame7")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# from tkinter import *
# Explicit imports to satisfy Flake8
import sqlite3
from tkinter import Tk, Canvas, Entry, Text, Button, messagebox, PhotoImage
import subprocess, sys

# Fuction to Log In a user
def user_login():
    conn = sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")
    c = conn.cursor()

    email = entry_1.get().strip()
    password = entry_2.get().strip()

    # Validate input
    if not email or not password:
        messagebox.showerror("Error", "Email and Password are required!")
        conn.close()
        return

    try:
        # Query to find user by email and password
        c.execute("SELECT id FROM Users_details WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()

        if user:
            user_id = user[0]  # Extract user_id
            messagebox.showinfo("Success", "Log in successful!")
            window.withdraw()
            subprocess.Popen([sys.executable, r"C:\Users\User\Documents\Ruxin file\build\car.py", str(user_id)])
        else:
            messagebox.showerror("Error", "Invalid email or password!")
            window.withdraw()
            subprocess.Popen(["python", r"C:\Users\User\Documents\Ruxin file\build\first_page.py"])
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()


# Login page
def show_log_in_page():
    global entry_1, entry_2

    canvas = Canvas(window, bg="#FFFFFF", height=679, width=1029, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(514.0, 339.0, image=image_image_1)

    canvas.create_text(251.0, 209.0, anchor="nw", text="Email:", fill="#000000", font=("Inter Bold", 48 * -1))

    entry_1 = Entry(bd=3, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Bold", 30))
    entry_1.place(x=251.0, y=266.0, width=555.0, height=46.0)
    canvas.create_text(251.0, 340.0, anchor="nw", text="Password:", fill="#000000", font=("Inter Bold", 48 * -1))


    entry_2 = Entry(bd=3, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*", font=("Inter Bold", 30))
    entry_2.place(x=251.0, y=391.0, width=555.0, height=46.0)

    canvas.create_text(365.0, 77.0, anchor="nw", text="Log in", fill="#000000", font=("Inter Bold", 60 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=user_login,
                      relief="flat")

    button_1.place(x=445.0, y=534.0, width=146.025390625, height=54.92308807373047)

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    # Initialize Tkinter window
    window = Tk()
    window.geometry("1029x679")
    window.configure(bg="#FFFFFF")
    show_log_in_page()
