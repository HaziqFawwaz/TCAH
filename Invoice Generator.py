import streamlit as st
from fpdf import FPDF
from datetime import date
import random

# Function to generate the invoice PDF
def generate_invoice(name, payment_due_date, package_basic_qty, package_advance_qty, package_full_day_qty, transit_basic_qty, transit_plus_qty, reg_qty, annual_qty):
    pdf = FPDF()
    pdf.add_page()

    # Title and Logo
    pdf.set_xy(10, 10)  # Reduced space from the top of the page
    pdf.set_font("Arial", "B", 35)
    pdf.cell(100, 40, "INVOICE", ln=False, align="L")  # Adjusted text position and size
    pdf.image("Logo Tadika.jpg", x=155, y=10, w=40, h=40)  # Adjusted logo size to align with text
    pdf.ln(5)

    # Line separator
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, 55, 200, 55)

    # Invoice details
    pdf.set_xy(10, 60)
    pdf.set_font("Arial", "B", size=12)  # Bold font for "Bill To"
    pdf.cell(100, 7, "Bill To:", ln=False, align="L")  # "Bill To" in bold
    pdf.cell(59, 7, "Invoice Date: ", ln=False, align="R")
    pdf.set_font("Arial", size=12)  # Bold font for "Bill To"
    pdf.cell(31, 7, f"{date.today().strftime('%d %B %Y')}", ln=True, align="R")
    pdf.set_font("Arial", size=12)  # Switch to regular font for the name
    pdf.cell(100, 7, f"{name}", ln=False, align="L")  # Name on the next line
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(59, 7, "Invoice Number: ", ln=False, align="R")
    pdf.set_font("Arial", size=12)
    pdf.cell(12, 7, f"{invoicenumber}", ln=True, align="R")
    # Address handling
    address_lines = address.split(",")  # Split the address by commas

    pdf.set_font("Arial", size=12)  # Font for address lines
    for i, line in enumerate(address_lines):
        if i < len(address_lines) - 1:
            pdf.cell(100, 7, line.strip() + ",", ln=True, align="L")  # Add comma except for last line
        else:
            pdf.cell(100, 7, line.strip(), ln=True, align="L")  # No comma for the last line


    # Add itemized table header
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, "Item", border=1, align="L")
    pdf.cell(30, 10, "Quantity", border=1, align="C")
    pdf.cell(40, 10, "Price per Unit (RM)", border=1, align="C")
    pdf.cell(40, 10, "Total (RM)", border=1, align="C")
    pdf.ln()

    # Item prices
    package_basic_price = 300  # Price for Package Basic
    package_advance_price = 380  # Price for Package Advance
    package_full_day_price = 460  # Price for Package Full Day
    transit_basic_price = 280  # Price for Transit Basic
    transit_plus_price = 330 # Price for Transit Plus
    reg_fee = 100
    annual_fee = 200

    # Add items to the table
    items = [
        ("Package Basic (7 am to 12.30 pm)", package_basic_qty, package_basic_price, package_basic_qty * package_basic_price),
        ("Package Advance (7 am to 3 pm)", package_advance_qty, package_advance_price, package_advance_qty * package_advance_price),
        ("Package Full Day (7 am to 5.30 pm)", package_full_day_qty, package_full_day_price, package_full_day_qty * package_full_day_price),
        ("Package Transit Basic", transit_basic_qty, transit_basic_price, transit_basic_qty * transit_basic_price),
        ("Package Transit Plus (Reading + Writing)", transit_plus_qty, transit_plus_price, transit_plus_qty * transit_plus_price),
        ("Registration Fee", reg_qty, reg_fee, reg_qty * reg_fee),
        ("Annual Fee", annual_qty, annual_fee, annual_qty * annual_fee),
    ]

    # Filter out items where quantity is 0
    filtered_items = [item for item in items if item[1] > 0]

    pdf.set_font("Arial", size=12)
    total = 0
    for item, qty, price, subtotal in filtered_items:
        pdf.cell(80, 10, item, border=1)
        pdf.cell(30, 10, str(qty), border=1, align="C")
        pdf.cell(40, 10, f"{price:.2f}", border=1, align="R")
        pdf.cell(40, 10, f"{subtotal:.2f}", border=1, align="R")
        pdf.ln()
        total += subtotal

    # Add total row
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Total (RM)", border=1, align="R")
    pdf.cell(40, 10, f"{total:.2f}", border=1, align="R")
    pdf.ln()

    # Add amount paid and balance due rows
    balance_due = total - amountpaid

    # Amount Paid row
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Amount Paid (RM)", border=1, align="R")
    pdf.cell(40, 10, f"{amountpaid:.2f}", border=1, align="R")
    pdf.ln()

    # Balance Due row
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Balance Due (RM)", border=1, align="R")
    pdf.cell(40, 10, f"{balance_due:.2f}", border=1, align="R")
    pdf.ln()

     # Add Pay To section below the table (right-aligned)
    pdf.ln(10)  # Add space after the total
    pdf.set_font("Arial","B", size=12)
    pdf.cell(110, 7, "Pay To:", ln=True, align="L")  # Title "Pay To"
    pdf.set_font("Arial", size=12)
    pdf.cell(110, 7, "Bank: MAYBANK", ln=True, align="L")  # Bank info
    pdf.cell(110, 7, "Payee: FATIN NAJWA BINTI MUHAMMAD FIRDAUS", ln=True, align="L")  # Payee info
    pdf.cell(110, 7, "Account No.: 156123816963", ln=True, align="L")  # Account info

    # Add Notes section aligned to the left
    pdf.ln(10)  # Add space after the total
    pdf.set_font("Arial","B", size=12)
    pdf.cell(110, 7, "Notes:", ln=True, align="L")  # Title "Pay To"
    # Draw rectangle for "Please pay to the above account..."
    pdf.set_font("Arial", size=12)
    pdf.cell(110, 7, f"Kindly make payment to the above account by {payment_due_date}.", ln=True, align="L")


    # Add a line at the bottom of the page
    pdf.set_draw_color(0, 0, 0)  # Set line color to black
    pdf.set_line_width(0.5)  # Set line thickness
    pdf.line(10, 270, 200, 270)  # Draw line (adjust Y-coordinate for position)

    # Add text below the line
    pdf.set_xy(10, 275)  # Position text below the line
    pdf.set_font("Arial", size=10)  # Set font size
    pdf.cell(0, 0, "This is a computer-generated invoice and no signature is required.", ln=False, align="C")

    # Save the PDF
    pdf.output("invoice.pdf")

# Function to generate the receipt PDF
def generate_receipt(name, package_basic_qty, package_advance_qty, package_full_day_qty, transit_basic_qty, transit_plus_qty, reg_qty, annual_qty):
    pdf = FPDF()
    pdf.add_page()

    # Title and Logo
    pdf.set_xy(10, 10)  # Reduced space from the top of the page
    pdf.set_font("Arial", "B", 35)
    pdf.cell(100, 40, "RECEIPT", ln=False, align="L")  # Adjusted text position and size
    pdf.image("Logo Tadika.jpg", x=155, y=10, w=40, h=40)  # Adjusted logo size to align with text
    pdf.ln(5)

    # Line separator
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, 55, 200, 55)

    # Receipt details
    pdf.set_xy(10, 60)
    pdf.set_font("Arial", "B", size=12)  # Bold font for "Bill To"
    pdf.cell(100, 7, "To:", ln=False, align="L")  # "To" in bold
    pdf.cell(59, 7, "Receipt Date: ", ln=False, align="R")
    pdf.set_font("Arial", size=12)  # Bold font for "Bill To"
    pdf.cell(31, 7, f"{date.today().strftime('%d %B %Y')}", ln=True, align="R")
    pdf.set_font("Arial", size=12)  # Switch to regular font for the name
    pdf.cell(100, 7, f"{name}", ln=False, align="L")  # Name on the next line
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(59, 7, "Receipt Number: ", ln=False, align="R")
    pdf.set_font("Arial", size=12)
    pdf.cell(12, 7, f"{receiptnumber}", ln=True, align="R")
    # Address handling
    address_lines = address.split(",")  # Split the address by commas

    pdf.set_font("Arial", size=12)  # Font for address lines
    for i, line in enumerate(address_lines):
        if i < len(address_lines) - 1:
            pdf.cell(100, 7, line.strip() + ",", ln=True, align="L")  # Add comma except for last line
        else:
            pdf.cell(100, 7, line.strip(), ln=True, align="L")  # No comma for the last line


    # Add itemized table header
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, "Item", border=1, align="L")
    pdf.cell(30, 10, "Quantity", border=1, align="C")
    pdf.cell(40, 10, "Price per Unit (RM)", border=1, align="C")
    pdf.cell(40, 10, "Total (RM)", border=1, align="C")
    pdf.ln()

    # Item prices
    package_basic_price = 300  # Price for Package Basic
    package_advance_price = 380  # Price for Package Advance
    package_full_day_price = 460  # Price for Package Full Day
    transit_basic_price = 280  # Price for Transit Basic
    transit_plus_price = 330 # Price for Transit Plus
    reg_fee = 100
    annual_fee = 200

    # Add items to the table
    items = [
        ("Package Basic (7 am to 12.30 pm)", package_basic_qty, package_basic_price, package_basic_qty * package_basic_price),
        ("Package Advance (7 am to 3 pm)", package_advance_qty, package_advance_price, package_advance_qty * package_advance_price),
        ("Package Full Day (7 am to 5.30 pm)", package_full_day_qty, package_full_day_price, package_full_day_qty * package_full_day_price),
         ("Package Transit Basic", transit_basic_qty, transit_basic_price, transit_basic_qty * transit_basic_price),
        ("Package Transit Plus (Reading + Writing)", transit_plus_qty, transit_plus_price, transit_plus_qty * transit_plus_price),
        ("Registration Fee", reg_qty, reg_fee, reg_qty * reg_fee),
        ("Annual Fee", annual_qty, annual_fee, annual_qty * annual_fee),
    ]

    # Filter out items where quantity is 0
    filtered_items = [item for item in items if item[1] > 0]

    pdf.set_font("Arial", size=12)
    total = 0
    for item, qty, price, subtotal in filtered_items:
        pdf.cell(80, 10, item, border=1)
        pdf.cell(30, 10, str(qty), border=1, align="C")
        pdf.cell(40, 10, f"{price:.2f}", border=1, align="R")
        pdf.cell(40, 10, f"{subtotal:.2f}", border=1, align="R")
        pdf.ln()
        total += subtotal

    # Add total row
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Total (RM)", border=1, align="R")
    pdf.cell(40, 10, f"{total:.2f}", border=1, align="R")
    pdf.ln()

    # Add amount paid and balance due rows
    balance_due = total - amountpaid

    # Amount Paid row
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Amount Paid (RM)", border=1, align="R")
    pdf.cell(40, 10, f"{amountpaid:.2f}", border=1, align="R")
    pdf.ln()

    # Balance Due row
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Balance Due (RM)", border=1, align="R")
    pdf.cell(40, 10, f"{balance_due:.2f}", border=1, align="R")
    pdf.ln()

    # Add a line at the bottom of the page
    pdf.set_draw_color(0, 0, 0)  # Set line color to black
    pdf.set_line_width(0.5)  # Set line thickness
    pdf.line(10, 270, 200, 270)  # Draw line (adjust Y-coordinate for position)

    # Add text below the line
    pdf.set_xy(10, 275)  # Position text below the line
    pdf.set_font("Arial", size=10)  # Set font size
    pdf.cell(0, 0, "This is a computer-generated receipt and no signature is required.", ln=False, align="C")

    # Save the PDF
    pdf.output("receipt.pdf")

# Sidebar
st.sidebar.title("Features")
option = st.sidebar.radio("Choose a feature:", ["Invoice Generator", "Receipt Generator"])

if option == "Invoice Generator":
    st.title("Invoice Generator")
    generate_clicked = False  # Track if the button was clicked

    with st.form("invoice_form"):
        name = st.text_input("Name")
        address = st.text_input("Address")
        invoicenumber = st.text_input("Invoice Number")
        amountpaid = st.number_input("Amount Paid", min_value=0.0, step=1.0)
        # Date Input for Payment Due Date
        payment_due_date = st.date_input("Select the payment due date:", min_value=date.today())

        st.write("Select quantities for each item:")
        package_basic_qty = st.number_input("Package Basic (RM 300 each)", min_value=0, step=1, value=0)
        package_advance_qty = st.number_input("Package Advance (RM 380 each)", min_value=0, step=1, value=0)
        package_full_day_qty = st.number_input("Package Full Day (RM 460 each)", min_value=0, step=1, value=0)
        transit_basic_qty = st.number_input("Transit Basic (RM 280 each)", min_value=0, step=1, value=0)
        transit_plus_qty = st.number_input("Transit Plus (RM 330 each)", min_value=0, step=1, value=0)
        reg_fee = st.number_input("Registration Fee (RM 100)", min_value=0, step=1, value=0)
        annual_fee = st.number_input("Annual Fee (RM 200)", min_value=0, step=1, value=0)

        # Buttons
        reset = st.form_submit_button("Reset Form")
        generate = st.form_submit_button("Generate Invoice")

        if reset:
            st.experimental_rerun()  # Reset the form by reloading the app

        if generate:
            generate_clicked = True  # Mark that the generate button was clicked

    if generate_clicked:
        if name.strip() == "":
            st.error("Please enter a name before generating the invoice.")
        else:
            generate_invoice(name, payment_due_date.strftime("%d/%m/%Y"), package_basic_qty, package_advance_qty, package_full_day_qty, transit_basic_qty, transit_plus_qty, reg_fee, annual_fee)
            with open("invoice.pdf", "rb") as file:
                st.download_button("Download Invoice", file, file_name="invoice.pdf")

elif option == "Receipt Generator":
    st.title("Receipt Generator")
    generate_clicked = False  # Track if the button was clicked

    with st.form("receipt_form"):
        name = st.text_input("Name")
        address = st.text_input("Address")
        receiptnumber = st.text_input("Receipt Number")
        amountpaid = st.number_input("Amount Paid", min_value=0.0, step=1.0)

        st.write("Select quantities for each item:")
        package_basic_qty = st.number_input("Package Basic (RM 300 each)", min_value=0, step=1, value=0)
        package_advance_qty = st.number_input("Package Advance (RM 380 each)", min_value=0, step=1, value=0)
        package_full_day_qty = st.number_input("Package Full Day (RM 460 each)", min_value=0, step=1, value=0)
        transit_basic_qty = st.number_input("Transit Basic (RM 280 each)", min_value=0, step=1, value=0)
        transit_plus_qty = st.number_input("Transit Plus (RM 330 each)", min_value=0, step=1, value=0)
        reg_fee = st.number_input("Registration Fee (RM 100)", min_value=0, step=1, value=0)
        annual_fee = st.number_input("Annual Fee (RM 200)", min_value=0, step=1, value=0)

        # Buttons
        reset1 = st.form_submit_button("Reset Form")
        generate1 = st.form_submit_button("Generate Receipt")

        if reset1:
            st.experimental_rerun()  # Reset the form by reloading the app

        if generate1:
            generate_clicked = True  # Mark that the generate button was clicked

    if generate_clicked:
        if name.strip() == "":
            st.error("Please enter a name before generating the receipt.")
        else:
            generate_receipt(name, package_basic_qty, package_advance_qty, package_full_day_qty, transit_basic_qty, transit_plus_qty, reg_fee, annual_fee)
            with open("receipt.pdf", "rb") as file:
                st.download_button("Download Receipt", file, file_name="receipt.pdf")


   


