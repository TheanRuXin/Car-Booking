
import customtkinter as ctk
import sqlite3, sys
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os

#Function to create the payment table in SQLite database
def create_payment_table():
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cardholder_name TEXT NOT NULL,
                        card_number TEXT NOT NULL,
                        expiry_date TEXT NOT NULL, 
                        cvv TEXT NOT NULL,
                        payment_amount FLOAT NOT NULL
                    )''')

    conn.commit()
    conn.close()

#Function to insert payment details into the database
def insert_payment_details(cardholder_name, card_number, expiry_date, cvv,payment_amount):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO payments (cardholder_name, card_number, expiry_date, cvv, payment_amount)
                    VALUES (?, ?, ?, ?, ?)''', (cardholder_name, card_number, expiry_date, cvv,payment_amount))
    conn.commit()
    conn.close()


#Function to generate the formatted receipt PDF without the total price
def generate_receipt (cardholder_name, card_number, expiry_date, payment_amount):
    # Define the file path for the receipt
    receipt_filename = f"receipt {cardholder_name.replace(' ', '_')}.pdf"

    c = canvas.Canvas (receipt_filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(30, height- 40,  "Car Rental Payment Receipt")

    # Line to separate the header
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line( 30, height-50, width-30, height - 50)

    # Payment details
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(30, height - 80, "Payment Details:")

    # Add Cardholder Name, Card Number, Expiry Date (masked Card Number)
    c.setFont("Helvetica", 14)
    c.drawString( 30, height-110,f"Cardholder Name: {cardholder_name}")
    c.drawString(30, height-140, f"Card Number: **** **** **** {card_number[-4:]}")
    c.drawString(30, height-170, f"Expiry Date: {expiry_date}")
    c.drawString(30, height-200, f"Payment Amount: RM {payment_amount}")
    # Add some space
    c.setFont("Helvetica",  12)
    c.drawString(30, height-250, "Thank you for your payment!")
    # Footer with the receipt filename
    c.setFont("Helvetica", 8)
    c.drawString(30, 40, "Car Rental")
    c.drawString( 30, 30, f"Receipt generated: {receipt_filename}")
    # Save the PDF
    c.save()
    # Show confirmation message for the receipt
    messagebox.showinfo("Receipt Generated",f"Your receipt has been saved as {receipt_filename}")

# Function to handle payment submission
def on_payment (cardholder_name, card_number, expiry_date, cvv, payment_amount):
    try:
        # Basic validation of fields
        if not cardholder_name or not card_number or not expiry_date or not cvv or not payment_amount:
            raise ValueError("All fields must be filled!")

        if len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("Card number must be 16 digits.")

        if len(cvv) != 3 or not cvv.isdigit():
            raise ValueError("CVV must be 3 digits.")

        if len(expiry_date) != 5 or expiry_date [2] != '/' or not expiry_date[:2].isdigit() or not expiry_date[3:].isdigit():
            raise ValueError("Expiry date must be in MM/YY format.")

        # Insert payment details into database
        insert_payment_details(cardholder_name, card_number, expiry_date, cvv, payment_amount)
        # Display success message
        messagebox.showinfo("Payment Successful",f"Payment for {cardholder_name} was successful!")
        # Generate receipt
        generate_receipt(cardholder_name, card_number, expiry_date, payment_amount)
    except ValueError as e:
        # Display error message
        messagebox.showerror("Payment Error", str(e))
    except Exception as e:
        # Handle unexpected errors
        messagebox.showerror("Payment Error",f"An unexpected error occurred: {str(e)}")

# Function to create and display the payment window
def payment_window():
    # Create the main window
    window = ctk.CTk()
    window.title("Credit/Debit Card Payment")
    window.geometry("400x450")

    # Create and display labels and entry fields for payment details
    cardholder_name_label = ctk.CTkLabel(window, text="Cardholder Name")
    cardholder_name_label.pack(pady=5)
    cardholder_name_entry = ctk.CTkEntry(window, placeholder_text="Enter Cardholder Name")
    cardholder_name_entry.pack(pady=5)

    card_number_label = ctk.CTkLabel(window, text="Card Number")
    card_number_label.pack(pady=5)
    card_number_entry = ctk.CTkEntry(window, placeholder_text="Enter Card Number")
    card_number_entry.pack(pady=5)

    expiry_date_label = ctk.CTkLabel(window, text="Expiry Date (MM/YY)")
    expiry_date_label.pack(pady=5)
    expiry_date_entry = ctk.CTkEntry(window, placeholder_text="Enter Expiry Date")
    expiry_date_entry.pack(pady=5)

    cvv_label = ctk.CTkLabel(window, text="CVV Number")
    cvv_label.pack(pady=5)
    cvv_entry = ctk.CTkEntry(window, placeholder_text="Enter CVV", show="*")
    cvv_entry.pack(pady=5)

    payment_amount_label = ctk.CTkLabel(window, text="Payment Amount (RM)")
    payment_amount_label.pack(pady=5)
    payment_amount_entry = ctk.CTkEntry(window, placeholder_text="Enter Payment Amount (RM)")
    payment_amount_entry.pack(pady=5)

    # Function to handle the Pay Now button click
    def on_pay_now():
        cardholder_name = cardholder_name_entry.get().strip()
        card_number = card_number_entry.get().strip()
        expiry_date = expiry_date_entry.get().strip()
        cvv = cvv_entry.get().strip()
        payment_amount = payment_amount_entry.get().strip()

        # Call the payment handler function
        on_payment(cardholder_name, card_number, expiry_date, cvv, payment_amount)
        # Pay Now Button

    pay_button = ctk.CTkButton(window, text="Pay", command = on_pay_now)
    pay_button.pack(pady=20)
    # Start the Tkinter event loop window.mainloop()
    window.mainloop()

# Main entry point for the program
if __name__ == "__main__":
    # Get booking_id and user_id from arguments
    if len(sys.argv) >= 3:
        booking_id = int(sys.argv[1])
        user_id = int(sys.argv[2])
    else:
        print("Error: Missing arguments.")
        sys.exit(1)
    create_payment_table()  # Create the payment table in the database if it doesn't exist
    payment_window()  # Open the payment window

