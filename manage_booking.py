import subprocess
import textwrap
from tkinter import Tk, Button, ttk, Label, messagebox, StringVar, Entry, Toplevel,Canvas,PhotoImage
import sqlite3,os,smtplib
from PIL import Image, ImageTk
from pathlib import Path
from email.mime.text import MIMEText
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\car rental booking system\build4\assets\frame11")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Connect to the database
def connect_db():
    conn = sqlite3.connect(r"C:\car rental booking system\Car-Booking\Users.db")
    return conn

def validate_date(date_text):
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None

# Function to fetch and display booking details based on date range
def show_booking_details(start_date=None, end_date=None, status=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = '''
        SELECT b.booking_id, c.make_and_model, b.customer_name,b.email, b.contact_number, 
               b.rental_start_date, b.rental_end_date, b.total_price, 
               COALESCE(julianday(b.rental_end_date) - julianday(b.rental_start_date), 0) AS days, b.status,c.image_path
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
    '''

    # Search by date range
    conditions = []
    params = []

    if start_date and end_date:
        conditions.append('DATE(b.rental_start_date) >= DATE(?) AND DATE(b.rental_end_date) <= DATE(?)')
        params.extend([start_date, end_date])
    elif start_date:  # Start date only
        conditions.append('DATE(b.rental_start_date) >= DATE(?)')
        params.append(start_date)
    elif end_date:  # End date only
        conditions.append('DATE(b.rental_end_date) <= DATE(?)')
        params.append(end_date)

    if status:
        conditions.append('b.status LIKE ?')
        params.append(status)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # Clear previous entries in the Treeview
    for item in treeview_bookings.get_children():
        treeview_bookings.delete(item)

    # Insert the fetched rows into the Treeview
    for row in rows:
        formatted_row = (
            row[0],  # ID
            row[1],  # Make & Model
            row[2],  # Customer Name
            row[3],  # Email
            row[4],  # Contact No.
            row[5],  # Start Date
            row[6],  # End Date
            row[7],  # Total Price
            row[8],  # No. of Days
            row[9]   # Status
        )
        treeview_bookings.insert("", "end", values=formatted_row)

def search_bookings():
    start_date_input = entry_start_date.get().strip()
    end_date_input = entry_end_date.get().strip()
    status = entry_status.get().strip()
    start_date = validate_date(start_date_input) if start_date_input else None
    end_date = validate_date(end_date_input) if end_date_input else None

    if start_date_input and not start_date:
        messagebox.showerror("Invalid Date",f"Start Date '{start_date_input}' is not in the correct format (YYYY-MM-DD).")
        return
    if end_date_input and not end_date:
        messagebox.showerror("Invalid Date", f"End Date '{end_date_input}' is not in the correct format (YYYY-MM-DD).")
        return
    if not start_date and not end_date and not status:
        messagebox.showwarning("Input Error", "Please enter at least one filter (date range or status).")
        return
    # Pass all filters to show_booking_details
    show_booking_details(start_date, end_date, status)

def open_booking_detail_window(booking_id):      #to approve/reject
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.booking_id, c.make_and_model, b.customer_name, b.email, b.contact_number,
               b.rental_start_date, b.rental_end_date, b.total_price, b.status
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.booking_id = ?
    ''', (booking_id,))

    booking = cursor.fetchone()
    conn.close()

    if booking:
        detail_window = Toplevel()
        detail_window.title("Booking Details")
        detail_window.geometry("900x900")

        Label(detail_window, text="Customer Booking Details", font=("Times New Roman", 16, "bold")).pack(pady=20)
        frame = ttk.Frame(detail_window)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Left align labels
        Label(frame, text="Booking ID:", font=("Times New Roman", 14)).grid(row=0, column=0, sticky="w", pady=5)
        Label(frame, text=booking[0], font=("Arial", 12)).grid(row=0, column=1, sticky="w", pady=5)

        Label(frame, text="Make & Model:", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w", pady=5)
        Label(frame, text=booking[1], font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=5)

        Label(frame, text="Customer Name:", font=("Times New Roman", 14)).grid(row=2, column=0, sticky="w", pady=5)
        Label(frame, text=booking[2], font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=5)

        Label(frame, text="Customer Email:", font=("Times New Roman", 14)).grid(row=3, column=0, sticky="w", pady=5)
        Label(frame, text=booking[3], font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=5)

        Label(frame, text="Contact No.:", font=("Times New Roman", 14)).grid(row=4, column=0, sticky="w", pady=5)
        Label(frame, text=booking[4], font=("Arial", 12)).grid(row=4, column=1, sticky="w", pady=5)

        Label(frame, text="Start Date:", font=("Times New Roman", 14)).grid(row=5, column=0, sticky="w", pady=5)
        Label(frame, text=booking[5], font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=5)

        Label(frame, text="End Date:", font=("Times New Roman", 14)).grid(row=6, column=0, sticky="w", pady=5)
        Label(frame, text=booking[6], font=("Arial", 12)).grid(row=6, column=1, sticky="w", pady=5)

        Label(frame, text="Total Price:", font=("Times New Roman", 14)).grid(row=7, column=0, sticky="w", pady=5)
        Label(frame, text="RM" + str(booking[7]), font=("Arial", 12)).grid(row=7, column=1, sticky="w", pady=5)

        Label(frame, text="Status:", font=("Times New Roman", 14)).grid(row=8, column=0, sticky="w", pady=5)
        Label(frame, text=booking[8], font=("Arial", 12)).grid(row=8, column=1, sticky="w", pady=5)

        Button(frame, text="Approve", command=lambda: update_booking_status(booking[0], "Approved", detail_window),
               bg="green", fg="black", font=("Arial",11)).grid(row=9, column=0, pady=10, sticky="ew")
        Button(frame, text="Reject", command=lambda: update_booking_status(booking[0], "Rejected", detail_window),
               bg="red", fg="black", font=("Arial",11)).grid(row=9, column=2, pady=10, sticky="ew")
        Button(frame, text="Payment Successful", command=lambda: update_booking_status(booking[0], "Payment Successful", detail_window),
               bg="yellow", fg="black", font=("Arial", 11)).grid(row=9, column=2, pady=10, sticky="ew")
        Button(frame, text="Return",command=lambda: update_booking_status(booking[0], "Car already return", detail_window),
               bg="blue", fg="black", font=("Arial", 11)).grid(row=9, column=3, pady=10, sticky="ew")



def update_booking_status(booking_id, status, detail_window):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET status = ? WHERE booking_id = ?', (status, booking_id))
    conn.commit()

    cursor.execute("SELECT email FROM bookings WHERE booking_id = ?", (booking_id,))
    to_email = cursor.fetchone()[0]
    conn.close()

    send_email(to_email,booking_id, status)

    show_booking_details()
    detail_window.destroy()  # Close the detail window
    messagebox.showinfo("Success", f"Booking {status.lower()} successfully!")

def send_email(to_email, booking_id, status):
    try:
        from_email = "jojolim0434@gmail.com"
        from_password = "diqe nxpk qsmd wsap"

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(from_email,from_password)

        subject = f"Car Booking {status.capitalize()}"
        body = textwrap.dedent(f"""
        Dear User,

        Your booking (ID: {booking_id}) has been {status}.
        {'Please proceed to payment.' if status == 'Approved' else 'We regret to inform you that your booking has been rejected.'}

        Regards,
        Car Rental Team
        """)
        msg = MIMEText(body)
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        server.send_message(msg)
        server.quit()

        messagebox.showinfo("Success","Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        messagebox.showerror("Error",f"Failed to send email: {e}")

def go_back():
    window.destroy()  # Close the current window
    subprocess.Popen(["python", "agency_panel.py"])  # Open the admin panel

def display_selected_image(event):
    selected_item = treeview_bookings.selection()
    if selected_item:
        item = treeview_bookings.item(selected_item)
        booking_id = item['values'][0]  # Get car ID from the selected row

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT c.image_path FROM cars c JOIN bookings b ON b.car_id = c.id WHERE b.booking_id = ?", (booking_id,))
        image_path = cursor.fetchone()

        if image_path and image_path[0]:
            try:
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

def view_booking_page():
    global window, treeview_bookings, entry_start_date, entry_end_date,entry_status,label_image
    window = Tk()
    window.geometry("1200x600")
    window.title("Car Rental - Booking Details")

    window.geometry("1221x773")
    window.title("Car Rental - Booking Details")

    canvas = Canvas(window, bg="#FFFFFF", height=773, width=1221, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(610.0, 386.0, image=image_image_1)

    canvas.create_text(600, 40, anchor="center", text="MANAGE BOOKING DETAILS", fill="#000000",
                       font=("Times New Roman ExtraBold", 18))

    # Input fields for date range search
    canvas.create_text(420.0, 80.0, anchor="nw", text="Start Date (YYYY-MM-DD):", fill="#000000",
                       font=("Inter Bold", 14 * -1))
    entry_start_date = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_start_date.place(x=610.0, y=80.0, width=180.0, height=22.0)

    canvas.create_text(420.0, 130.0, anchor="nw", text="End Date (YYYY-MM-DD):", fill="#000000",
                       font=("Inter Bold", 14 * -1))
    entry_end_date = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_end_date.place(x=610.0, y=130.0, width=180.0, height=22.0)

    canvas.create_text(420.0, 180.0, anchor="nw", text="Status:", fill="#000000", font=("Inter Bold", 14 * -1))
    entry_status = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_status.place(x=610.0, y=180.0, width=180.0, height=22.0)

    button_search = Button(text="Search", command=search_bookings, bg="blue", fg="white", font=("Arial", 11))
    button_search.place(x=560.0, y=230.0, width=100.0, height=30.0)

    # Define the columns for the Treeview
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Make & Model", "Customer Name", "Customer Email",
                                                      "Contact No.", "Start Date", "End Date", "Total Price",
                                                      "No. of Days", "Status"), show="headings")

    scrollbar_x = ttk.Scrollbar(window, orient="horizontal", command=treeview_bookings.xview)
    scrollbar_x.place(x=25, y=580, width=850, height=20)
    treeview_bookings.configure(xscrollcommand=scrollbar_x.set)

    for col in treeview_bookings["columns"]:
        treeview_bookings.heading(col, text=col)

    # Define column widths
    for col in treeview_bookings["columns"]:
        treeview_bookings.column(col, width=100, anchor="center")

    treeview_bookings.place(x=25, y=280, width=850, height=300)  # add treeview to GUI

    # Bind double-click event to open booking details
    treeview_bookings.bind("<Double-1>", lambda event: open_booking_detail_window(
        treeview_bookings.item(treeview_bookings.selection())['values'][0]))
    treeview_bookings.bind("<<TreeviewSelect>>", display_selected_image)

    button_back = Button(text="Back", command=go_back, bg="orange", fg="black", font=("Arial", 11))
    button_back.place(x=560.0, y=630.0, width=100.0, height=30.0)

    label_image = Label(window)
    label_image.place(x=900, y=280, width=300, height=300)

    window.mainloop()


view_booking_page()
