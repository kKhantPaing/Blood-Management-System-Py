""" Main application file for the Blood Management System """
import sqlite3
import os
import sys
import getpass
from time import sleep
from db_operations import (
    create_connection,
    setup_database,
    insert_user,
    is_username_exists,
    login_user,
    change_user_password,
    reset_database,
    get_available_blood_units
)
from models import User
from utils import is_strong_password


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
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def first_time_setup(conn):
    """ Set up the database and create an admin user on first run """
    clear_screen()
    setup_database(conn)
    add_new_user(conn)
    print("Database setup complete. You can now log in with your new user.")


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
        print("5. Emergency Blood Request")
        print("6. Settings")
        print("7. Logout")
        print("8. Exit")
        choice = input("Enter your choice: ")
        clear_screen()
        if choice == '1':
            print("Available Blood Units:")
            available_units = get_available_blood_units(conn)
            print("+------------+-----------------+")
            print("| Blood Type | Available Units |")
            print("+------------+-----------------+")
            for blood_type, units in available_units:
                print(f"| {blood_type:<10} | {units:>15} |")
            print("+------------+-----------------+")
        elif choice == '2':
            # Code to add new blood unit
            pass
        elif choice == '3':
            # Code to add new donor
            pass
        elif choice == '4':
            # Code to view donor information
            pass
        elif choice == '5':
            # Code to handle emergency blood request
            pass
        elif choice == '6':
            # Code to settings view
            settings_view(conn, current_user)
        elif choice == '7':
            print("Logging out...")
            sleep(3)
            default_view(conn)
            break
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


def settings_view(conn, current_user):
    """ Display settings view for the current user """
    while True:
        print(f"Settings for {current_user}:")
        print("\nMenu:")
        print("1. Change Password")
        print("2. Add New User")
        print("3. Reset Database")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")
        clear_screen()
        if choice == '1':
            current_password = getpass.getpass(prompt="Enter current password: ").strip()
            if not login_user(conn, current_user, current_password):
                print("Incorrect current password. Please try again.")
                continue
            new_password = getpass.getpass(prompt="Enter new password: ").strip()
            if not is_strong_password(new_password):
                print("Password must be at least 8 characters long and include uppercase letters, lowercase letters, and numbers.")
                continue
            # Code to update the user's password in the database
            change_user_password(conn, current_user, new_password)
        elif choice == '2':
            add_new_user(conn)
        elif choice == '3':
            confirm = input("Are you sure you want to reset the database? This action cannot be undone. (yes/no): ")
            if confirm.lower() == 'yes':
                reset_database(conn)
                print("Database has been reset. Returning to database setup.")
                first_time_setup(conn)
                break
            else:
                print("Database reset cancelled.")
        elif choice == '4':
            print("Returning to main menu...")
            sleep(2)
            auth_user_view(conn, current_user)
            break
        else:
            print("Invalid choice. Please try again.")


def clear_screen():
    """ Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def add_new_user(conn):
    """ Add a new user to the system """
    name = input("Enter user's name: ")
    username = input("Enter username: ").strip().lower()
    password = getpass.getpass(prompt="Enter password: ").strip()
    if is_username_exists(conn, username):
        print("Username already exists. Please choose a different username.")
        return
    if not is_strong_password(password):
        print("Password must be at least 8 characters long and include uppercase letters, lowercase letters, and numbers.")
        return
    try:
        user = User(name, username, password)
        insert_user(conn, user)
        print("User created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")


if __name__ == "__main__":
    main()
