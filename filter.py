from tkinter import Tk, Canvas, Entry, Button, StringVar, filedialog, OptionMenu, Label, ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

def connect_db():
    conn = sqlite3.connect('car_details.db')
    return conn

def show_filtered_cars(make_and_model=None, color=None, seating_capacity=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM cars_details WHERE 1=1 "
    params = []

    if make_and_model:
        query += "AND make_and_model = ?"
        params.append(make_and_model)
    if color:
        query += " AND color = ?"
        params.append(color)
    if seating_capacity:
        query += " AND seating_capacity >= ?"
        params.append(seating_capacity)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_filter_options(window):
    # Create dropdowns for brand, color, and seats
    make_and_model_var = StringVar(window)
    color_var = StringVar(window)
    seating_capacity_var = StringVar(window)

    brands = ["Toyota Camry", "Honda Civic", "BMW 3 Series", "Ford Focus", "Audi A4"]  # Populate with actual brands from your database
    colors = ["White","Black","Grey","Silver"]  # Populate with actual colors from your database
    seats_options = [2, 4, 5, 7]  # Example seat capacities

    ttk.Label(window, text="Select Brand:").pack()
    brand_dropdown = ttk.Combobox(window, textvariable=make_and_model_var, values=brands)
    brand_dropdown.pack()

    ttk.Label(window, text="Select Color:").pack()
    color_dropdown = ttk.Combobox(window, textvariable=color_var, values=colors)
    color_dropdown.pack()

    ttk.Label(window, text="Minimum Seats:").pack()
    seats_dropdown = ttk.Combobox(window, textvariable=seating_capacity_var, values=seats_options)
    seats_dropdown.pack()

    # Filter button
    Button(window, text="Filter", command=lambda: filter_cars(make_and_model_var.get(), color_var.get(), seating_capacity_var.get())).pack()

    return make_and_model_var, color_var, seating_capacity_var

def filter_cars(make_and_model, color, seating_capacity):
    # Clear current Treeview entries
    for item in treeview_bookings.get_children():
        treeview_bookings.delete(item)

    # Fetch filtered car details
    filtered_cars = show_filtered_cars(make_and_model if make_and_model else None, color if color else None, int(seating_capacity) if seating_capacity else None)

    # Display filtered results
    for car in filtered_cars:
        treeview_bookings.insert("", "end", values=car)

def show_booking_details():
    # This function should fetch all booking details and display them initially
    bookings = show_filtered_cars()  # Fetch all cars as a starting point
    for booking in bookings:
        treeview_bookings.insert("", "end", values=booking)

def booking_info_page():
    window = Tk()
    window.geometry("1000x500")
    window.title("Customer Booking Details")

    global treeview_bookings
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg. No.", "Make & Model", "Customer Name",
                                                      "Contact No.", "Start Date", "End Date",
                                                      "Total Price", "Status"), show="headings")

    # Define headers for Treeview
    for header in treeview_bookings['columns']:
        treeview_bookings.heading(header, text=header)
        treeview_bookings.column(header, anchor="center", width=100)

    treeview_bookings.pack(pady=20, fill="x")

    # Display filter options
    display_filter_options(window)

    # Load initial booking details
    show_booking_details()

    window.mainloop()

if __name__ == "__main__":
    booking_info_page()