
import customtkinter as ctk
import sqlite3, sys, smtplib, os
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#Function to create the payment table in SQLite database
def create_payment_table():
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        booking_id INTEGER,
                        customer_email TEXT,
                        cardholder_name TEXT NOT NULL,
                        card_number TEXT NOT NULL,
                        expiry_date TEXT NOT NULL, 
                        cvv TEXT NOT NULL,
                        payment_amount FLOAT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES Users_details(id),
                        FOREIGN KEY(booking_id) REFERENCES bookings(id)
                    )''')

    conn.commit()
    conn.close()

def get_user_email_from_bookings(booking_id):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM bookings WHERE booking_id = ?", (booking_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

#Function to insert payment details into the database
def insert_payment_details(user_id, booking_id, user_email, cardholder_name, card_number, expiry_date, cvv,payment_amount):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO payments (user_id, booking_id, customer_email, cardholder_name, card_number, expiry_date, cvv, payment_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (user_id, booking_id, user_email, cardholder_name, card_number, expiry_date, cvv,payment_amount))
    conn.commit()
    conn.close()

#Function to generate the formatted receipt PDF without the total price
def generate_receipt (user_email, cardholder_name, card_number, expiry_date, payment_amount):
    os.makedirs("receipts", exist_ok=True)
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
    c.drawString( 30, height-110,f"Email: {user_email}")
    c.drawString( 30, height-140,f"Cardholder Name: {cardholder_name}")
    c.drawString(30, height-170, f"Card Number: **** **** **** {card_number[-4:]}")
    c.drawString(30, height-200, f"Expiry Date: {expiry_date}")
    c.drawString(30, height-230, f"Payment Amount: RM {payment_amount}")
    # Add some space
    c.setFont("Helvetica",  12)
    c.drawString(30, height-280, "Thank you for your payment!")
    # Footer with the receipt filename
    c.setFont("Helvetica", 8)
    c.drawString(30, 40, "Car Rental")
    c.drawString( 30, 30, f"Receipt generated: {receipt_filename}")
    # Save the PDF
    c.save()
    # Show confirmation message for the receipt
    messagebox.showinfo("Receipt Generated",f"Your receipt has been saved as {receipt_filename}")
    send_receipt_via_email(user_email, receipt_filename)

# Function to handle payment submission
def on_payment (user_email, cardholder_name, card_number, expiry_date, cvv, payment_amount):
    try:
        # Basic validation of fields
        if not cardholder_name or not card_number or not expiry_date or not cvv or not payment_amount:
            raise ValueError("All fields must be filled!")

        if len(card_number) != 16 or not card_number.isdigit():
            print(f"Card number entered: '{card_number}' (Length: {len(card_number)})")
            raise ValueError("Card number must be 16 digits.")

        if len(cvv) != 3 or not cvv.isdigit():
            raise ValueError("CVV must be 3 digits.")

        if len(expiry_date) != 5 or expiry_date [2] != '/' or not expiry_date[:2].isdigit() or not expiry_date[3:].isdigit():
            raise ValueError("Expiry date must be in MM/YY format.")

        booking_id = int(sys.argv[1])  # Ensure booking_id is passed
        user_id = int(sys.argv[2])  # Ensure user_id is passed

        # Insert payment details into database
        insert_payment_details(user_id, booking_id, user_email, cardholder_name, card_number, expiry_date, cvv, float(payment_amount))
        # Mark booking as paid
        mark_booking_as_paid(booking_id)
        # Display success message
        messagebox.showinfo("Payment Successful",f"Payment for {cardholder_name} was successful!")
        # Generate receipt
        generate_receipt(user_email, cardholder_name, card_number, expiry_date, payment_amount)

    except ValueError as e:
        # Display error message
        messagebox.showerror("Payment Error", str(e))
    except Exception as e:
        # Handle unexpected errors
        messagebox.showerror("Payment Error",f"An unexpected error occurred: {str(e)}")

def get_payment_amount(booking_id):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT total_price FROM bookings WHERE booking_id = ?", (booking_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def mark_booking_as_paid(booking_id):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = 'Paid' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()

def send_receipt_via_email(user_email, receipt_filename):
    try:
        # Email sender and receiver
        sender_email = "jojolim0434@gmail.com"  # Replace with your email
        sender_password = "diqe nxpk qsmd wsap"        # Replace with your email password or app password
        receiver_email = user_email

        # Email subject and body
        subject = "Car Rental Payment Receipt"
        body = f"""
        Dear Customer,

        Thank you for your payment! Please find your receipt attached to this email.

        Regards,
        Car Rental Team
        """

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the body
        msg.attach(MIMEText(body, 'plain'))

        # Attach the receipt file
        with open(receipt_filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(receipt_filename)}')
            msg.attach(part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"Receipt sent successfully to {user_email}!")
        messagebox.showinfo("Receipt Sent", f"Receipt sent successfully to {user_email}!")
    except Exception as e:
        print(f"Failed to send receipt: {e}")
        messagebox.showerror("Error", f"Failed to send receipt: {e}")

# Function to create and display the payment window
def payment_window():
    # Create the main window
    window = ctk.CTk()
    window.title("Credit/Debit Card Payment")
    window.geometry("400x450")

    # Fetch payment amount based on booking_id
    booking_id = int(sys.argv[1])
    payment_amount = get_payment_amount(booking_id)

    if payment_amount is None:
        messagebox.showerror("Error", "Failed to retrieve payment amount for this booking.")
        return

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

    payment_amount_label = ctk.CTkLabel(window, text=f"Payment Amount:RM{payment_amount}")
    payment_amount_label.pack(pady=5)
    payment_amount_entry = ctk.CTkEntry(window, placeholder_text="Enter Payment Amount (RM)")
    payment_amount_entry.pack(pady=5)

    # Function to handle the Pay Now button click
    def on_pay_now():
        cardholder_name = cardholder_name_entry.get().strip()
        card_number = card_number_entry.get().strip()
        expiry_date = expiry_date_entry.get().strip()
        cvv = cvv_entry.get().strip()
        entered_payment_amount = payment_amount_entry.get().strip()
        user_email = get_user_email_from_bookings(booking_id)

        if not user_email:
            messagebox.showerror("Error", "Email not found for this booking.")
            return
        # Validate entered payment amount
        try:
            entered_payment_amount = float(entered_payment_amount)
            if entered_payment_amount != payment_amount:
                raise ValueError(f"Payment amount must be RM {payment_amount}.")
            # Call payment function with fetched payment amount
            on_payment(user_email, cardholder_name, card_number, expiry_date, cvv, payment_amount)

        except ValueError as e:
            messagebox.showerror("Payment Error", str(e))

    # Pay Now Button
    pay_button = ctk.CTkButton(window, text="Pay", command = on_pay_now)
    pay_button.pack(pady=20)
    # Start the Tkinter event loop window.mainloop()
    window.mainloop()

# Main entry point for the program
if __name__ == "__main__":
    try:
        booking_id = int(sys.argv[1])  # This will raise ValueError if invalid
        user_id = int(sys.argv[2])  # Second argument: user_id
    except IndexError:
        print("Error: Missing arguments.")
        sys.exit(1)
    except ValueError:
        print(f"Error: Invalid argument values passed (booking_id and user_id must be integers).")
        sys.exit(1)

    create_payment_table()  # Create the payment table in the database if it doesn't exist
    payment_window()  # Open the payment window

