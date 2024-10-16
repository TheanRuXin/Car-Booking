
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,messagebox
import subprocess
import sqlite3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\profile\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#connect with database
def connect_db():
    conn = sqlite3.connect(r'C:\Users\User\Documents\Ruxin file\build\adminpage\build\Users.db') # Use raw string for the path
    return conn

def load_user_data(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, phone_number, email FROM Users WHERE id = ?", (user_id,))
    return cursor.fetchone() # result

def save_profile(window,user_id):
    username = entry_1.get()
    phone_number = entry_2.get()
    email = entry_3.get()
    password = entry_4.get()
    confirm_password = entry_5.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Users 
            SET username = ?, phone_number = ?, email = ?, password = ?
            WHERE id = ?  -- Assuming id is the unique identifier
        ''', (username, phone_number, email, password,user_id))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Warning", "No user found with that email.")
        else:
            messagebox.showinfo("Success", "Profile updated successfully!")

        conn.close()
        window.destroy()# Close the edit window after saving
        subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\profile\build\Profile.py"])
    except Exception as error: 
        print(f"An error occurred: {error}")  # This will show the error in the console
        messagebox.showerror("Error", f"An error occurred: {error}") 

def cancel_profile(window):
    window.destroy()
    subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\profile\build\Profile.py"])
    
def show_edit_file_page(user_id):
    global entry_1, entry_2, entry_3, entry_4, entry_5
    user_data = load_user_data(user_id)

    if user_data:
        username, phone_number, email = user_data
    else:
        messagebox.showerror("Error","User not found.")
        return


    window = Tk()
    window.geometry("1029x679")
    window.configure(bg = "#FFFFFF")

    canvas = Canvas(window,bg = "#FFFFFF",height = 679,width = 1029,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(0.0,1.0,1034.0,139.0,fill="#DFDFDF",outline="")
    canvas.create_rectangle(0.0,1.0,1029.0,139.0,fill="#DFDFDF",outline="")

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(73.0,66.0,image=image_image_1)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0,
                      command=lambda: print("button_1 clicked"), relief="flat")
    button_1.place(x=517.0, y=51.0, width=62.0, height=40.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"),relief="flat")
    button_2.place(x=579.0,y=51.0,width=74.0,height=40.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(image=button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked"),relief="flat")
    button_3.place( x=653.0,y=51.0,width=69.0,height=40.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(image=button_image_4,borderwidth=0,highlightthickness=0,command=lambda: print("button_4 clicked"),relief="flat")
    button_4.place( x=722.0,y=51.0,width=74.0,height=40.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(image=button_image_5,borderwidth=0,highlightthickness=0,command=lambda: print("button_5 clicked"),relief="flat")
    button_5.place(x=944.0,y=47.0,width=49.0,height=49.0)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(image=button_image_6,borderwidth=0,highlightthickness=0,command=lambda: print("button_6 clicked"),relief="flat")
    button_6.place(x=800.0,y=51.0,width=122.0,height=40.0)

    canvas.create_text(157.0,164.0,anchor="nw",text="Name",fill="#000000",font=("RobotoRoman Regular", 16 * -1))

    entry_image_1 = PhotoImage( file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(515.0, 208.0, image=entry_image_1)
    entry_1 = Entry(bd=0,bg="#F5F5F5",fg="#000716",highlightthickness=0)
    entry_1.place(x=177.0,y=188.0,width=676.0,height=38.0)

    canvas.create_text(157.0,244.0,anchor="nw",text="Phone Number",fill="#000000",font=("RobotoRoman Regular", 16 * -1))
    entry_image_2 = PhotoImage( file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(515.0,288.0,image=entry_image_2)
    entry_2 = Entry(bd=0,bg="#F5F5F5",fg="#000716",highlightthickness=0)
    entry_2.place(x=177.0,y=268.0,width=676.0,height=38.0)

    canvas.create_text(156.0,324.0,anchor="nw",text="Email",fill="#000000",font=("RobotoRoman Regular", 16 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(514.0,368.0,image=entry_image_3)
    entry_3 = Entry(bd=0,bg="#F5F5F5",fg="#000716",highlightthickness=0)
    entry_3.place(x=176.0,y=348.0,width=676.0,height=38.0)
    
    canvas.create_text(157.0,404.0,anchor="nw",text="Password",fill="#000000",font=("RobotoRoman Regular", 16 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
    515.0,448.0,image=entry_image_4)
    entry_4 = Entry(bd=0,bg="#F5F5F5",fg="#000716",highlightthickness=0,show="*")
    entry_4.place(x=177.0,y=428.0,width=676.0,height=38.0)

    canvas.create_text(157.0,483.0,anchor="nw",text="Confirm Password",fill="#000000",font=("RobotoRoman Regular", 16 * -1))

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(515.0,527.0,image=entry_image_5)
    entry_5 = Entry(bd=0,bg="#F5F5F5",fg="#000716",highlightthickness=0,show="*")
    entry_5.place(x=177.0,y=507.0,width=676.0,height=38.0)

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(image=button_image_7,borderwidth=0,highlightthickness=0,command=lambda:save_profile(window,user_id),relief="flat")
    button_7.place(x=639.0,y=594.0,width=122.0,height=40.0)

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(image=button_image_8,borderwidth=0,highlightthickness=0,command=lambda:cancel_profile(window),relief="flat")
    button_8.place(x=258.0,y=594.0,width=122.0,height=40.0)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    user_id = 1
    show_edit_file_page(user_id)