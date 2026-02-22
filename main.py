""" Main application file for the Blood Management System """
import os
from db_operations import (
    create_connection,
    create_tables,
    insert_donor,
    get_blood_availability,
    login_user
)
from models import User

DB_NAME = "blood_management.db"


def main():
    """ Main function to run the Blood Management System """
    db_exists = os.path.exists(DB_NAME) 
    try:
        conn = create_connection(DB_NAME)
        if conn is not None:
            with conn:
                if not db_exists:
                    first_time_setup(conn)
                default_view(conn)
        else:
            print("Error! cannot create the database connection.")
    except Exception as e:
        print(f"An error occurred: {e}")


def first_time_setup(conn):
    """ Set up the database and create an admin user on first run """
    create_tables(conn)
    name = input("Enter your name: ")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    try:
        user = User(name, username, password)
        insert_donor(conn, user)
        print("Admin user created successfully. You can now log in with these credentials.")
    except Exception as e:
        print(f"Error creating admin user: {e}")


def default_view(conn):
    """ Display the default view for users after login """
    print("Welcome to the Blood Management System!")
    # Here you can add code to interact with the user, such as a menu system
    # For example:
    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. View Available Blood Types")
        print("3. Exit")
        choice = input("Enter your choice: ")
        clear_screen()
        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login_user(conn, username, password):
                print(f"Welcome back, {username}!")
                # Display user-specific options here
                auth_user_view(conn)
            else:
                print("Invalid credentials. Please try again.")
                default_view(conn)  # Restart the login process
        elif choice == '2':
            print("Available Blood Types:")
            available_blood_types = get_blood_availability(conn)
            for blood_type in available_blood_types:
                print(f"Blood Type: {blood_type[0]}, Available Count: {blood_type[1]}")
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def auth_user_view(conn):
    """ Display user-specific view after successful login """


def clear_screen():
    """ Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

              
if __name__ == "__main__":
    main()
