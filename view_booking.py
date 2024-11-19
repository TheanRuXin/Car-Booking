from pathlib import Path
import subprocess
import sqlite3
import sys
from tkinter import Tk, Canvas, Entry, Toplevel, Text, Button, PhotoImage, ttk, messagebox, Label
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\car rental booking system\build4\assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Connect to the database
def connect_db():
    conn = sqlite3.connect(r"C:\car rental booking system\Car-Booking\Users.db")
    return conn

def show_booking_details(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(''' 
        SELECT b.booking_id, b.customer_name, c.make_and_model,
               b.rental_start_date, b.rental_end_date, b.total_price,
               COALESCE(julianday(b.rental_end_date) - julianday(b.rental_start_date), 0) AS days, b.status, c.image_path, b.user_id
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.user_id = ?
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    # Clear previous bookings from the Treeview
    for item in treeview_bookings.get_children():
        treeview_bookings.delete(item)

    # Insert the rows for the logged-in user
    for row in rows:
        treeview_bookings.insert("", "end", values=row)

def on_treeview_select(event):
    selected_item = treeview_bookings.selection()

    if selected_item:
        item = treeview_bookings.item(selected_item)
        booking_status = item['values'][7]

        # Enabling or disabling buttons based on booking status
        if booking_status.lower() == "Approved":
            clear_button.config(state="disabled")

        elif booking_status.lower() == "pending":
            clear_button.config(state="normal")

        else:
            clear_button.config(state="disabled")
    else:
        messagebox.showwarning("Selection Error", "No booking selected.")
        return None

def open_payment_window():
    selected_item = treeview_bookings.selection()

    if selected_item:
        item = treeview_bookings.item(selected_item)
        booking_id = item['values'][0]  # Get the Booking ID from the selected row
        user_id = item['values'][9]  # Get the user ID from the selected row (ensure it's available)
        booking_status = item['values'][7].strip().lower()
        customer_name = item['values'][1]

        if booking_status != "approved":
            messagebox.showwarning("Action Not Allowed", "Payment can only be made for approved bookings.")
            return

        try:
            # Open the payment window
            subprocess.Popen(
                [sys.executable, r"C:\car rental booking system\Car-Booking\payment.py", str(booking_id), str(user_id)])
            messagebox.showinfo("Payment", f"Payment window opened for {customer_name}.")

            # Disable the payment button after initiating payment
            payment_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open payment window: {e}")
    else:
        messagebox.showwarning("No Booking Selected", "Please select a booking first.")

def clear_booking():
    selected_item = treeview_bookings.selection()
    if selected_item:
        item = treeview_bookings.item(selected_item)
        booking_id = item['values'][0]
        booking_status = item['values'][7]

        if booking_status.lower() != "pending":
            messagebox.showwarning("Action Not Allowed", "Only pending bookings can be cleared.")
            return

        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this booking?"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))
            conn.commit()
            conn.close()

            # Refresh the booking details after deletion
            show_booking_details(user_id)
            messagebox.showinfo("Success", "Booking cleared successfully!")
    else:
        messagebox.showwarning("Selection Error", "Please select a booking to clear.")

def display_selected_image():
    selected_item = treeview_bookings.selection()
    if selected_item:
        item = treeview_bookings.item(selected_item)
        make_and_model = item['values'][2]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM cars WHERE make_and_model = ?", (make_and_model,))
        image_path = cursor.fetchone()

        if image_path and image_path[0]:
            try:
                img = Image.open(image_path[0])
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                label_image.config(image=img)
                label_image.image = img
            except Exception as e:
                print(f"Error loading image: {e}")
                label_image.config(image='')

        else:
            label_image.config(image='', text="No image found.")
        conn.close()

def go_back(user_id):
    window.withdraw()
    subprocess.Popen([sys.executable, "Profile.py", str(user_id)])

def promo_button():
    window.withdraw()
    subprocess.Popen(["python", r"C:\car rental booking system\Car-Booking\promo.py"])

def cars_button():
    window.withdraw()
    subprocess.Popen(["python", r"C:\car rental booking system\Car-Booking\car.py"])

def profile_page():
    window.withdraw()
    subprocess.Popen(["python", r"C:\car rental booking system\Car-Booking\Profile.py"])

window = Tk()
window.geometry("1221x773")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=773, width=1221, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 1221.0, 113.0, fill="#DFDFDF", outline="")

treeview_bookings = ttk.Treeview(window, columns=("Booking ID", "Customer Name", "Make & Model", "Start Date", "End Date", "Total Price", "No. of Days", "Status"), show="headings")
treeview_bookings.heading("Booking ID", text="ID")
treeview_bookings.heading("Customer Name", text="Customer Name")
treeview_bookings.heading("Make & Model", text="Make & Model")
treeview_bookings.heading("Start Date", text="Start Date")
treeview_bookings.heading("End Date", text="End Date")
treeview_bookings.heading("Total Price", text="Total Price (RM)")
treeview_bookings.heading("No. of Days", text="No. of Days")
treeview_bookings.heading("Status", text="Status")

treeview_bookings.column("Booking ID", width=50, anchor="center")
treeview_bookings.column("Customer Name", width=80, anchor="center")
treeview_bookings.column("Make & Model", width=130, anchor="center")
treeview_bookings.column("Start Date", width=90, anchor="center")
treeview_bookings.column("End Date", width=90, anchor="center")
treeview_bookings.column("Total Price", width=100, anchor="center")
treeview_bookings.column("No. of Days", width=90, anchor="center")
treeview_bookings.column("Status", width=90, anchor="center")

treeview_bookings.place(x=25, y=280, width=850, height=300)

treeview_bookings.bind("<<TreeviewSelect>>", on_treeview_select)
treeview_bookings.bind("<<TreeviewSelect>>", lambda event: display_selected_image())



Button(window, text="Refresh Bookings", command=lambda: show_booking_details(user_id), bg="red", fg="black", font=("KaiseiDecol Medium", 16 * -1)).place(x=25, y=600, width=150, height=50)
clear_button=Button(window, text="Clear Booking", command=clear_booking, bg="orange", fg="black", font=("KaiseiDecol Medium", 16 * -1))
clear_button.place(x=220, y=600, width=150, height=50)
Button(window, text="Back", command=lambda: go_back(user_id), bg="yellow", fg="black", font=("KaiseiDecol Medium", 16 * -1)).place(x=425, y=600, width=50, height=50)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(86.0, 57.0, image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: profile_page(), relief="flat")
button_1.place(x=1126.0, y=31.0, width=49.0, height=49.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: promo_button(), relief="flat")
button_4.place(x=854.0, y=30.0, width=90.0, height=52.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: cars_button(), relief="flat")
button_5.place(x=784.0, y=30.0, width=70.0, height=52.0)

canvas.create_text(56.0, 168.0, anchor="nw", text="View Booking", fill="#000000", font=("KaiseiDecol Medium", 40 * -1))

label_image = Label(window)
label_image.place(x=900, y=280, width=300, height=300)

payment_button = Button(window, text="Make Payment", bg="blue", fg="white", font=("Arial", 14), command=open_payment_window)
payment_button.place(x=650, y=600, width=150, height=50)

current_user_id = 123
user_id = current_user_id if len(sys.argv) <= 1 else int(sys.argv[1])

show_booking_details(user_id)
window.mainloop()
