import pymysql
import os
import uuid
import sys
from passenger import view_passenger
from staff import view_staff, edit_staff_main
from train_schedule import view_train_schedule, edit_train_main

dbconect = pymysql.connect(
    host="localhost", 
    user='dbuser', 
    password='password', 
    database='rmsdb'
)

cursor = dbconect.cursor()

# Generate unique token
def gen_token():
    return str(uuid.uuid4())

# Save token locally
def save_token_locally(token):
    with open('token.txt', 'w') as file:
        file.write(token)

# Check if token already exists and get unique token
def get_token():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as file:
            return file.read().strip()  # Strip any extra spaces or newlines
    return None

# Import all tokens from the database
def get_all_tokens():
    cursor.execute("SELECT token FROM users")
    tokens = cursor.fetchall()
    return [t[0] for t in tokens]

# Save token to database for a specific user
def save_token(username, token):
    token = token.strip()  # Remove leading/trailing spaces from the token
    cursor.execute("UPDATE users SET token=%s WHERE username=%s", (token, username))
    dbconect.commit()

# Login with username and password
def user_login(username, password):
    cursor.execute("SELECT username, password FROM users WHERE username=%s AND password=%s", (username, password))
    access = cursor.fetchone()
    return access is not None

# Main login system
def login_system():
    local_token = get_token()
    if local_token:
        all_tokens = get_all_tokens()
        if local_token in all_tokens:
            print("Welcome back!")
            dashboard()
        return

    # If no valid token, ask for username and password
    username = input("Enter username: ")
    password = input("Enter password: ")
    if user_login(username, password):
        new_token = gen_token().strip()  # Generate and strip any spaces from the new token
        save_token(username, new_token)
        save_token_locally(new_token)
        print(f"Login successful. Welcome, {username}")
        dashboard()
        return
    else:
        print("Invalid username or password")
        return
    
def dashboard():
    keep_running = True  # Flag to control the loop
    while keep_running:
        print(''' 
              1. View Passenger Data
              2. View Staff Data
              3. Edit Staff Data
              4. View Train Schedule
              5. Edit Train Schedule
              6. Logout''')
        choice = int(input('What do you want to do?: '))
        
        if choice == 1:
            view_passenger()
        elif choice == 2:
            view_staff()
        elif choice == 3:
            edit_staff_main()
        elif choice == 4:
            view_train_schedule()
        elif choice == 5:
            edit_train_main()
        elif choice == 6:
            print("Logging out...")
            os.remove('token.txt')  # Remove the local token file
            dbconect.close()  # Close the database connection
            keep_running = False  # Set flag to False to exit the loop
        else:
            print("Invalid choice, please select again.")
            