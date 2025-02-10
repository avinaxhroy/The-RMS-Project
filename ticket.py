from PIL import Image, ImageDraw, ImageFont
import os
import random
import pandas as pd
from tabulate import tabulate
import pymysql


dbconect = pymysql.connect(
    host="localhost", 
    user='dbuser', 
    password='password', 
    database='rmsdb'
)

cursor = dbconect.cursor()

distance_data = {
    ("DELHI", "MUMBAI"): 1400,
    ("DELHI", "CHENNAI"): 2200,
    ("DELHI", "KOLKATA"): 1500,
    ("MUMBAI", "CHENNAI"): 1300,
    ("MUMBAI", "KOLKATA"): 2000,
    ("CHENNAI", "KOLKATA"): 1650,
    ("DELHI", "BANGALORE"): 2150,
    ("MUMBAI", "BANGALORE"): 980,
    ("CHENNAI", "BANGALORE"): 350,
    ("KOLKATA", "BANGALORE"): 1870,
    ("DELHI", "HYDERABAD"): 1550,
    ("MUMBAI", "HYDERABAD"): 710,
    ("CHENNAI", "HYDERABAD"): 630,
    ("KOLKATA", "HYDERABAD"): 1480,
    ("BANGALORE", "HYDERABAD"): 570,
    ("DELHI", "LUCKNOW"): 550,
    ("LUCKNOW", "VARANASI"): 320,
    ("VARANASI", "PATNA"): 250,
    ("PATNA", "RANCHI"): 330,
    ("PATNA", "GAYA"): 100,
    ("LUCKNOW", "KANPUR"): 90,
    ("KANPUR", "AGRA"): 270,
    ("AGRA", "DELHI"): 230,
    ("PATNA", "BHUBANESWAR"): 720,
    ("PATNA", "KOLKATA"): 580
}

#export passenger data to databse
def send_passenger_data(name, start, end, cost, travel_date):
    query=f"insert into passengers(name, cost, destination, travel_date) values('{name}', '{cost}', '{start} To {end}', '{travel_date}')"
    cursor.execute(query)
    dbconect.commit()


def generate_short_ticket_number():
    uni_code=""
    alpha_list = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for j in range(11):
        uni_code+=random.choice(alpha_list)
    return uni_code



# Function to get distance between two places
def get_distance(origin, destination):
    route = (origin, destination)
    reverse_route = (destination, origin)
    if route in distance_data:
        return distance_data[route]
    elif reverse_route in distance_data:
        return distance_data[reverse_route]
    else:
        return None  # Return None if distance is not found




def generate_ticket(visitor_name, start, end, total_dist, cost, travel_date):
    # Get the directory where the script is located
    script_dir = os.path.abspath(os.path.dirname(__file__))  # Absolute path for safety

    # Construct the full path to the ticket image file
    ticket_path = os.path.join(script_dir, "ticket_tmt.png")

    # Load the sample ticket image
    ticket = Image.open(ticket_path)  # Make sure this file exists

    # Prepare to draw on the image
    draw = ImageDraw.Draw(ticket)

    # Load a font
    font_path = os.path.join("font", "CourierPrime-Bold.ttf")
    font = ImageFont.truetype(font_path, 35)  # Adjust the font size as needed

    #Unique Ticket Number
    ticket_number = generate_short_ticket_number()

    # Define positions for the text on the ticket
    name_position = (30, 130)  # Example coordinates, adjust as needed
    destination_position = (782, 222)  # Example coordinates, adjust as needed
    distance_position = (782, 302)  # Example coordinates, adjust as needed
    cost_position = (782, 382)  # Example coordinates, adjust as needed
    date_position = (782, 462)  # Example coordinates, adjust as needed
    ticnumber_position=(782,130)

    # Draw the text onto the image
    draw.text(name_position, f"NAME OF PASSENGER: \n{visitor_name.upper()}", fill="black", font=font)
    draw.text(destination_position, f"ROUTE:\n{start.upper()} TO {end.upper()}", fill="black", font=font)
    draw.text(distance_position, f"DISTANCE:\n{total_dist} KM", fill="black", font=font)
    draw.text(cost_position, f"COST:\nRs. {cost:.2f}", fill="black", font=font)
    draw.text(date_position, f"TRAVEL DATE:\n{travel_date}", fill="black", font=font)
    draw.text(ticnumber_position, f"TICKET NUMBER:\n{ticket_number}", fill="black", font=font)

    # Save the new ticket
    os.makedirs('tickets', exist_ok=True)
    ticket_path = os.path.join('tickets', f"{visitor_name}_ticket.png")
    ticket.save(ticket_path)
    print(f"Your ticket has been saved as {ticket_path}")




def book_ticket():
    print("Available Routes:")
    for routes in distance_data:
        print(f"{routes[0]} to {routes[1]}")

    start = input("From where you want to start journey?: ").upper()
    end = input("Where you want to go?: ").upper()
    total_dist = get_distance(start, end)

    if total_dist is None:
        print("Sorry, the route you selected is not available.")
        return

    cost = total_dist * 2.5
    print(f"Total Distance: {total_dist} KM \nTotal Charges: Rs. {cost:.2f}")

    proceed1 = input('Do you want to continue? (Yes or No): ').upper()
    if proceed1 in ('Y', 'YES'):
        visitor_name = input('Enter Your Name: ').upper()
        travel_date = input("On which date you want to travel?(YYYY-MM-DD): ")
        modpayment = input("Select your mode of payment:\n1. UPI\n2. Net Banking\n3. Cash \n: ")
        customer_dat={'Name':visitor_name,'Destination':f'{start} TO {end}','Distance':f'{total_dist} KM','Cost':cost,'Date':travel_date}
        customer_data=pd.DataFrame(customer_dat,index=[0])
        print(tabulate(customer_data, headers='keys', tablefmt='grid'))
        confirm_booking = input("Do you want to confirm your booking? (Yes or No): ").upper()
        if confirm_booking in ('Y', 'YES'):
            print("Your Ticket Booked Successfully")
            generate_ticket(visitor_name, start, end, total_dist, cost, travel_date)
            send_passenger_data(visitor_name, start, end, cost, travel_date)
        else:
            print("Booking not confirmed.")
    else:
        print("Booking cancelled.")