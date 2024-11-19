
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, messagebox,Entry, Text, Button, PhotoImage,ttk,Label,Toplevel
from PIL import Image, ImageTk
import subprocess,sys

import sqlite3,os
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Ruxin file\build\assets\frame5")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_history_table():
    try:
        conn = sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS History (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                user_id INTEGER,
                customer_name TEXT,
                email TEXT,
                contact_number TEXT,     
                date_of_birth TEXT,    
                rental_start_date TEXT,    
                rental_end_date TEXT,
                promotion TEXT,
                total_price REAL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY(car_id) REFERENCES cars_details(id),
                FOREIGN KEY(user_id) REFERENCES Users_details(id)
            )
        ''')
        conn.commit()
        print("History table created successfully.")
    except sqlite3.Error as e:
        print("Error creating History table:", e)
    finally:
        conn.close()

create_history_table()

def connect_db():
    return sqlite3.connect(r"C:\Users\User\Documents\Ruxin file\build\Car_Rental.db")

def show_history_details(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT c.registration_number, c.make_and_model,
               h.rental_start_date, h.rental_end_date, h.total_price,
               COALESCE(julianday(h.rental_end_date) - julianday(h.rental_start_date), 0) AS days
        FROM History h
        JOIN cars_details c ON h.car_id = c.id
        WHERE h.user_id = ?
    ''',(user_id,))
    rows = cursor.fetchall()
    conn.close()

    for item in treeview_history.get_children():
        treeview_history.delete(item)

    for row in rows:
        treeview_history.insert("", "end", values=row)


def display_selected_image(event):
    selected_item = treeview_history.selection()
    if selected_item:
        item = treeview_history.item(selected_item)
        reg_num = item['values'][0]  # Get car ID from the selected row

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT image_path FROM cars_details WHERE registration_number = \'{reg_num}\'")

        image_path = cursor.fetchone()

        print(image_path)
        if image_path and image_path[0]:
            print(1)
            try:
                print(2)
                img = Image.open(image_path[0])
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)

                # Display the image
                label_image.config(image=img)
                label_image.image = img
            except Exception as e:
                print(f"Error loading image: {e}")
                label_image.config(image='')
        else:
            label_image.config(image='')

def open_rating_window(user_id,car_id):
    if not car_id:
        messagebox.showerror("Error", "No car selected!")
        return
    window.withdraw()
    subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\build\rating.py",str(user_id),str(car_id)])
def get_selected_car_id():
    selected_item = treeview_history.selection()
    if selected_item:
        item = treeview_history.item(selected_item)
        reg_num = item['values'][0]  # Get registration number from the selected row

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cars_details WHERE registration_number = ?", (reg_num,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]  # Return the car ID
    return None

def promo_button(user_id):
    window.destroy()
    subprocess.Popen(["python",r"C:\Users\User\Documents\Ruxin file\build\promo.py",str(user_id)])

def cars_button(user_id):
    window.destroy()
    subprocess.Popen(["python", r"C:\Users\User\Documents\Ruxin file\build\car.py",str(user_id)])

def profile_button(user_id):
    window.destroy()
    subprocess.Popen(["python", "Profile.py",str(user_id)])

window = Tk()
window.geometry("1221x773")
window.configure(bg = "#FFFFFF")
canvas = Canvas(window,bg = "#FFFFFF",height = 773,width = 1221,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0,0.0,1221.0,113.0,fill="#DFDFDF",outline="")

treeview_history = ttk.Treeview(window, columns=("Reg. No.", "Make & Model",
                                                  "Start Date", "End Date", "Total Price",
                                                  "No. of Days"), show="headings")

# Define headings for the Treeview
treeview_history.heading("Reg. No.", text="Reg. No.")
treeview_history.heading("Make & Model", text="Make & Model")
treeview_history.heading("Start Date", text="Start Date")
treeview_history.heading("End Date", text="End Date")
treeview_history.heading("Total Price", text="Total Price (RM)")
treeview_history.heading("No. of Days", text="No. of Days")
# Define column widths and alignment
treeview_history.column("Reg. No.", width=80, anchor="center")
treeview_history.column("Make & Model", width=130, anchor="center")
treeview_history.column("Start Date", width=90, anchor="center")
treeview_history.column("End Date", width=90, anchor="center")
treeview_history.column("Total Price", width=100, anchor="center")
treeview_history.column("No. of Days", width=90, anchor="center")

# Pack Treeview
treeview_history.place(x=25, y=280, width=850, height=300)

treeview_history.bind("<<TreeviewSelect>>", display_selected_image)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(86.0,57.0,image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=lambda:profile_button(user_id),relief="flat")
button_1.place(x=1126.0,y=31.0,width=49.0,height=49.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4,borderwidth=0,highlightthickness=0,command=lambda:promo_button(user_id),relief="flat")
button_4.place(x=1010.0,y=24.0,width=90.0,height=52.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5,borderwidth=0,highlightthickness=0,command=lambda: cars_button(user_id),relief="flat")
button_5.place(x=917.0,y=24.0,width=70.0,height=52.0)

canvas.create_text(56.0,168.0,anchor="nw",text="History",fill="#000000",font=("KaiseiDecol Medium", 40 * -1))

label_image = Label(window)
label_image.place(x=900, y=280, width=300, height=300)

button_rating = Button(window, text="Rating", command=lambda:open_rating_window(user_id,get_selected_car_id()), bg="red", fg="yellow",font=("KaiseiDecol Medium", 16 * -1))
button_rating.place(x=25,y=600,width=150,height=50)

if len(sys.argv) < 2:
    messagebox.showerror("Error", "User ID not provided.")
    sys.exit(1)

user_id = int(sys.argv[1])
car_id = int(sys.argv[1])
show_history_details(user_id)
window.resizable(False, False)
window.mainloop()
