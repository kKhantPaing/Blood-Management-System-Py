""" Main application file for the Blood Management System """
import sqlite3
import os, sys
from db_operations import(
    create_connection,
    setup_database,
    insert_user,
    login_user,
    reset_database,
    get_available_blood_units
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
    clear_screen()
    setup_database(conn)
    name = input("Enter your name: ")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    try:
        user = User(name, username, password)
        insert_user(conn, user)
        print("Admin user created successfully. You can now log in with these credentials.")
    except sqlite3.Error as e:
        print(f"Error creating admin user: {e}")


def default_view(conn):
    """ Display the default view for users who are not logged in """
    print("Welcome to the Blood Management System!")
    # Here you can add code to interact with the user, such as a menu system
    # For example:
    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. View Available Blood Units")
        print("3. Exit")
        choice = input("Enter your choice: ")
        clear_screen()
        if choice == '1':
            username = input("Enter your username: ").lower()
            password = input("Enter your password: ")
            current_user = login_user(conn, username, password)
            if current_user:
                # Display user-specific options here
                auth_user_view(conn, current_user)
                break
            else:
                print("Invalid credentials. Please try again.")
        elif choice == '2':
            print("Available Blood Units:")
            available_units = get_available_blood_units(conn)
            print("+------------+-----------------+")
            print("| Blood Type | Available Units |")
            print("+------------+-----------------+")
            for blood_type, units in available_units:
                print(f"| {blood_type:<10} | {units:>15} |")
            print("+------------+-----------------+")
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


def auth_user_view(conn, current_user):
    """ Display user-specific view after successful login """
    while True:
        print(f"Welcome back, {current_user}!")
        print("\nMenu:")
        print("1. View Available Blood Units")
        print("2. Add New Blood Unit")
        print("3. Add New Donor")
        print("4. View Donor Information")
        print("5. Add User")
        # choice = input("Enter your choice: ")
        # clear_screen()
        


def clear_screen():
    """ Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

              
if __name__ == "__main__":
    main()
