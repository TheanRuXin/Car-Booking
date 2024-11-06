
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sqlite3
from PIL import Image, ImageTk
import subprocess, sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\car rental booking system\build4\assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def promo_button(window):
    window.destroy()
    subprocess.Popen(["python","promo.py"])

def profile_button(window):
    window.destroy()
    subprocess.Popen(["python", "Profile.py"])

def connect_db():
    conn = sqlite3.connect(r"C:\car rental booking system\Car-Booking\Users.db")
    return conn

def open_booking_page(car_id):
    window.withdraw()
    # Pass car_id as an argument
    subprocess.Popen([sys.executable, "booking_form.py", str(car_id)])

# Modified search_cars to display directly on canvas
def search_cars():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT id, make_and_model, daily_rate, seating_capacity, car_type, transmission_type, image_path FROM cars WHERE 1=1"
    parameters = []

    car_model = car_model_entry.get().lower()
    min_price = min_price_entry.get()
    max_price = max_price_entry.get()
    seats = seats_entry.get()

    if car_model:
        query += " AND LOWER(make_and_model) LIKE ?"
        parameters.append(f"%{car_model}%")
    if min_price:
        query += " AND daily_rate >= ?"
        parameters.append(int(min_price))
    if max_price:
        query += " AND daily_rate <= ?"
        parameters.append(int(max_price))
    if seats:
        query += " AND seating_capacity = ?"
        parameters.append(int(seats))


    cursor.execute(query, parameters)
    filtered_cars = cursor.fetchall()
    conn.close()

    car_details = [{'id': car[0],'brand': car[1], 'price': car[2], 'seats': car[3], 'car_type': car[4], 'transmission': car[5], 'image': car[6]} for car in filtered_cars]
    display_car_details(car_details)

def display_car_details(car_data):
    canvas.delete("car_detail")  # Clear previous details
    canvas.image_references = [] # Create a list to hold image references

    coords = [
        (316.0, 140.0, 578.0, 309.0),
        (614.0, 140.0, 877.0, 309.0),
        (913.0, 140.0, 1175.0, 309.0),
        (316.0, 353.0, 578.0, 522.0),
        (614.0, 353.0, 877.0, 522.0),
        (913.0, 353.0, 1175.0, 522.0),
        (316.0, 566.0, 578.0, 735.0),
        (614.0, 566.0, 877.0, 735.0),
        (913.0, 566.0, 1175.0, 735.0),
    ]

    for i, car in enumerate(car_data):
        if i >= len(coords):
            break  # Exit if more cars than the available rectangles

        x1, y1, x2, y2 = coords[i]

        # Load the image
        if car['image']:
            try:
                car_image = Image.open(car['image'])
                car_image = car_image.resize((150, 110), Image.LANCZOS)
                car_image = ImageTk.PhotoImage(car_image)
                canvas.image_references.append(car_image)
                canvas.create_image(x1 + 110, y1 + 2, anchor="nw", image=car_image, tags="car_detail")

            except Exception as e:
                print(f"Error loading image for {car['brand']}: {e}")

        # Display car details
        canvas.create_text((x1 + 20, y1 + 80), text=f"{car['brand']}", font=("Helvetica", 13, "bold"), anchor="nw", tags="car_detail")
        canvas.create_text((x1 + 20, y1 + 100), text=f"Price: RM{car['price']}", font=("Helvetica", 11), anchor="nw", tags="car_detail")
        canvas.create_text((x1 + 20, y1 + 120), text=f"Seats: {car['seats']}, Car Type: {car['car_type']}", font=("Helvetica", 11), anchor="nw", tags="car_detail")
        canvas.create_text((x1 + 20, y1 + 140), text=f"Transmission: {car['transmission']}", font=("Helvetica", 11), anchor="nw", tags="car_detail")

        book_button = Button(
            window,
            text="BOOK",
            font=("Helvetica", 10),
            bg="black",
            fg="white",
            command=lambda car_id=car['id']:open_booking_page(car_id)
        )
        canvas.create_window(x1 + 200, y1 + 130, anchor="nw", window=book_button, tags="car_detail")

def load_all_cars():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, make_and_model, daily_rate, seating_capacity, car_type, transmission_type,image_path FROM cars")
    car_data = cursor.fetchall()
    conn.close()

    car_details = [{'id': car[0], 'brand': car[1], 'price': car[2], 'seats': car[3], 'car_type': car[4], 'transmission': car[5], 'image': car[6]}for car in car_data]
    display_car_details(car_details)


window = Tk()

window.geometry("1221x773")
window.configure(bg = "#FFFFFF")

canvas = Canvas(window,bg = "#FFFFFF",
    height = 773,
    width = 1221,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1221.0,
    113.0,
    fill="#DFDFDF",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    86.0,
    57.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: profile_button(window),
    relief="flat"
)
button_1.place(
    x=1126.0,
    y=31.0,
    width=49.0,
    height=49.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=969.0,
    y=36.0,
    width=132.0,
    height=40.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: promo_button(window),
    relief="flat"
)
button_4.place(
    x=854.0,
    y=30.0,
    width=90.0,
    height=52.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=784.0,
    y=30.0,
    width=70.0,
    height=52.0
)

canvas.create_text(
    92.0,
    305.0,
    anchor="nw",
    text="Car Model:",
    fill="#000000",
    font=("KaiseiDecol Medium", 16 * -1)
)

canvas.create_text(
    54.0,
    266.0,
    anchor="nw",
    text="Filter:",
    fill="#000000",
    font=("KaiseiDecol Medium", 18 * -1)
)

canvas.create_text(
    47.0,
    143.0,
    anchor="nw",
    text="Cars",
    fill="#000000",
    font=("KaiseiDecol Medium", 40 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    142.5,
    356.5,
    image=entry_image_1
)
car_model_entry = Entry(
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
car_model_entry.place(
    x=54.0,
    y=339.0,
    width=177.0,
    height=33.0
)

canvas.create_text(
    80.0,
    388.0,
    anchor="nw",
    text="Min Price(RM):",
    fill="#000000",
    font=("KaiseiDecol Medium", 16 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    140.5,
    439.5,
    image=entry_image_2
)
min_price_entry = Entry(
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
min_price_entry.place(
    x=52.0,
    y=422.0,
    width=177.0,
    height=33.0
)

canvas.create_text(
    116.0,
    553.0,
    anchor="nw",
    text="Seats:",
    fill="#000000",
    font=("KaiseiDecol Medium", 16 * -1)
)


seats_entry = Entry(
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
seats_entry.place(
    x=52.0,
    y=588.0,
    width=177.0,
    height=32.0
)

canvas.create_text(
    79.0,
    470.0,
    anchor="nw",
    text="Max Price(RM):",
    fill="#000000",
    font=("KaiseiDecol Medium", 16 * -1)
)

max_price_entry = Entry(
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
max_price_entry.place(
    x=52.0,
    y=505.0,
    width=177.0,
    height=32.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: search_cars(),
    relief="flat"
)
button_6.place(
    x=102.0,
    y=671.0,
    width=77.0,
    height=28.0
)

canvas.create_rectangle(
    33.0,
    240.0,
    249.0,
    730.0,
    outline="#BEB4B4",
    width=2
)


image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    446.0,
    194.0,
    image=image_image_2
)
canvas.create_rectangle(316.0, 140.0, 578.0, 309.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(614.0, 140.0, 877.0, 309.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(913.0, 140.0, 1175.0, 309.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(316.0, 353.0, 578.0, 522.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(614.0, 353.0, 877.0, 522.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(913.0, 353.0, 1175.0, 522.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(316.0, 566.0, 578.0, 735.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(614.0, 566.0, 877.0, 735.0, fill="#FFFDFD", outline="grey", width=1)
canvas.create_rectangle(913.0, 566.0, 1175.0, 735.0, fill="#FFFDFD", outline="grey", width=1)

load_all_cars()

window.resizable(False, False)
window.mainloop()
