from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.action_chains import ActionChains
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime

# def calculate_time_difference(given_date):
#     # Parse the given date (format: YYYY-MM-DD HH:MM:SS)
#     given_date = datetime.strptime(given_date, "%Y-%m-%d %H:%M:%S")
    
#     # Get the current date and time
#     current_date = datetime.now()
    
#     # Calculate the difference
#     time_difference = current_date - given_date
    
#     # Extract days, seconds, hours, and minutes
#     days = time_difference.days
#     seconds = time_difference.seconds
#     hours = seconds // 3600
#     minutes = (seconds % 3600) // 60
#     remaining_seconds = seconds % 60
    
#     # Convert the entire time difference to seconds
#     total_seconds = time_difference.total_seconds()
    
#     # Print the results
#     print(f"Time Difference: {abs(days)} days, {abs(hours)} hours, {abs(minutes)} minutes, {abs(remaining_seconds)} seconds")
#     print(f"Total Time Difference in Seconds: {abs(int(total_seconds))} seconds")
#     return abs(int(total_seconds))

# # Example usage
# given_date = "2025-01-29 00:00:00"  # Replace with your date
# total_seconds = calculate_time_difference(given_date)
# time.sleep(total_seconds)

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the login page
driver.get("https://oas.iitmandi.ac.in/instituteprocess/common/login.aspx")

# Maximize the browser window (optional)
driver.maximize_window()

# Locate the username and password fields
username_field = driver.find_element(By.ID, "txtLoginId")
password_field = driver.find_element(By.ID, "txtPassword")

# Enter the username and password
username = "b24350"  # Replace with the actual username
password = os.environ['pass']  # Replace with the actual password

username_field.send_keys(username)
password_field.send_keys(password)

time.sleep(1)
login_button = driver.find_element(By.ID, "btnLogin")

# Click the login button
login_button.click()
time.sleep(1)

# Navigate directly to the Seat Booking page
seat_booking_url = "https://oas.iitmandi.ac.in/instituteprocess/Facility/BusSeatReservation.aspx"
driver.get(seat_booking_url)

time.sleep(1)
print('started date filing')

# travel_date_input.send_keys("30012025")

# Fill the Travel Date
travel_date_field = driver.find_element(By.ID, "txtFromDate").click()
travel_date_field1 = driver.find_element(By.ID, "txtFromDate")
# travel_date_field.clear()  # Clear any pre-filled value
for i in range(10):
    travel_date_field1.send_keys(Keys.ARROW_LEFT) 
travel_date_field1.send_keys("13-02-2025")  # Enter the travel date

time.sleep(1)
print('started route filing')
# Select the Route from the dropdown
route_dropdown = Select(driver.find_element(By.ID, "ddlRoute"))
route_dropdown.select_by_value("1")  # Select "North Campus -To- Mandi (via South)"

time.sleep(1)
print('started time filing')
# Select the Schedule from the dropdown
schedule_dropdown = Select(driver.find_element(By.ID, "ddlTiming"))
schedule_dropdown.select_by_value("1022")  # Select "07:00 PM"
print('finished time filing')
# # Add a short delay to observe the interaction
time.sleep(1.5)  # Adjust as needed

# Select the Bus No. from the dropdown
bus_no_dropdown = Select(driver.find_element(By.ID, "ddlBus"))
bus_no_dropdown.select_by_value("3182")  # Select "BUS(A)"
time.sleep(1.5)

# Check the checkbox with ID 'checkbox14'
checkbox = driver.find_element(By.ID, "checkbox15")

# Check if the checkbox is not already selected, and if not, click to select it
if not checkbox.is_selected():
    checkbox.click()
time.sleep(.5)
# Click the Save button with ID 'lnkSave'
save_button = driver.find_element(By.ID, "lnkSave")
save_button.click()

def send_confirmation_email(recipient_email, travel_date, route, bus_no):
    sender_email = "b24350@students.iitmandi.ac.in"  # Replace with your email
    sender_password = os.environ['emailPass']  # Replace with your email password

    # Create the email content
    subject = "Bus Seat Booking Confirmation"
    body = f"""
    Dear Student,

    Your bus seat has been successfully booked. Below are your booking details:

    Travel Date: {travel_date}
    Route: {route}
    Bus No: {bus_no}

    Thank you for booking with us!

    Best Regards,
    IIT Mandi Transport Team
    """

    # Set up the MIME message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Set up the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Encrypt connection
            server.login(sender_email, sender_password)  # Login with email and password
            server.sendmail(sender_email, recipient_email, message.as_string())  # Send email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Call this function with the recipient email and booking details
recipient_email = "b24350@students.iitmandi.ac.in"  # Replace with student's email
travel_date = "30/01/2025"
route = "North Campus -To- Mandi (via South)"
bus_no = "BUS(A)"

send_confirmation_email(recipient_email, travel_date, route, bus_no)

time.sleep(10)  # Keep the browser open for 10 seconds (adjust as needed)