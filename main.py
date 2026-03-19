""" Main application file for the Blood Management System """
import sqlite3
import os
import sys
import getpass
from time import sleep
from datetime import datetime, timedelta
from db_operations import (
    create_connection,
    get_all_donors_info,
    get_blood_types_donation_by_id,
    get_blood_units_by_type,
    insert_donor,
    setup_database,
    insert_user,
    insert_blood_donation,
    is_username_exists,
    login_user,
    change_user_password,
    reset_database,
    get_available_blood_units,
    update_blood_donation_status,
    update_blood_donation_by_id
)
from models import User
from utils import hash_password, is_strong_password


DB_NAME = "blood_management.db"

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


def main():
    """ Main function to run the Blood Management System """
    db_exists = os.path.exists(DB_NAME)
    try:
        conn = create_connection(DB_NAME)
        if conn is not None:
            with conn:
                if not db_exists:
                    first_time_setup(conn)
                else:
                    # Check for expired blood donations and update availability
                    update_blood_donation_status(conn, datetime.now().strftime("%Y-%m-%d"))
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
            current_user = login_user(conn, username, hash_password(password))

            if current_user:
                # Display user-specific options here
                auth_user_view(conn, current_user)
                break
            else:
                print("Invalid credentials. Please try again.")

        elif choice == '2':
            available_units_view(conn)

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
        print("2. Request Blood Units by Blood Type")
        print("3. Add New Blood Unit")
        print("4. Add New Donor")
        print("5. View Donor Information")
        print("6. Emergency Blood Request")
        print("7. Settings")
        print("8. Logout")
        print("9. Exit")

        choice = input("Enter your choice: ")

        clear_screen()

        if choice == '1':
            available_units_view(conn)

        elif choice == '2':
            print("Request Blood Units by Blood Type: \n")
            while True:
                blood_type = input("Enter required blood type: ")
                if blood_type in BLOOD_TYPES:
                    break
                else:
                    print("Invalid blood type. Please enter a valid blood type.")
            while True:
                try:
                    units = int(input("Enter number of units: "))
                    if units < 0:
                        print("Units cannot be negative. Please enter a valid number.")
                    else:
                        break
                except ValueError:
                    print("Invalid input for units. Please enter a number.")

            available_units = get_blood_units_by_type(conn, blood_type)

            if available_units >= units:
                update_blood_donation_usage(conn, blood_type, units)
                print(f"Request successful! {units} units of {blood_type} blood have been allocated to you.")
            else:
                print(f"Sorry, only {available_units} units of {blood_type} blood are available. Your request cannot be fulfilled.")
                print("Do you want to use them? (yes/no)")
                use_available = input().strip().lower()
                if use_available == 'yes':
                    update_blood_donation_usage(conn, blood_type, available_units)
                    print(f"Request successful! {available_units} units of {blood_type} blood have been allocated to you.")
            print("Press Enter to return to the main menu...")
            input()

        elif choice == '3':
            donar_id = input("Enter donor ID: ")
            while True:
                blood_type = input("Enter blood type: ")
                if blood_type in BLOOD_TYPES:
                    break
                else:
                    print("Invalid blood type. Please enter a valid blood type.")
            while True:
                try:
                    units = int(input("Enter number of units: "))
                    if units < 0:
                        print("Units cannot be negative. Please enter a valid number.")
                    else:
                        break
                except ValueError:
                    print("Invalid input for units. Please enter a number.")
            donation_date = input("Enter donation date (YYYY-MM-DD): ")
            # Assuming blood expires after 42 days
            expiration_date = datetime.strptime(donation_date, "%Y-%m-%d") + timedelta(days=42)
            blood_donation = (donar_id, blood_type, units, donation_date, expiration_date)
            if insert_blood_donation(conn, blood_donation):
                print("Blood donation added successfully.")
            print("Press Enter to return to the main menu...")
            input()

        elif choice == '4':
            donar_name = input("Enter donor's name: ")
            donar_phone = input("Enter donor's phone: ")
            donar_address = input("Enter donor's address: ")
            donar_dob = input("Enter donor's date of birth (YYYY-MM-DD): ")
            donar_gender = input("Enter donor's gender: ")
            while True:
                donar_blood_type = input("Enter donor's blood type: ")
                if donar_blood_type in BLOOD_TYPES:
                    break
                else:
                    print("Invalid blood type. Please enter a valid blood type.")
            last_donation_date = input("Enter last donation date (YYYY-MM-DD) or leave blank if never donated: ")
            is_urgent_available = input("Is the donor urgently available? (yes/no): ").strip().lower() == 'yes'
            donor = (donar_name, donar_phone, donar_address, donar_dob, donar_gender, donar_blood_type,
                     last_donation_date, is_urgent_available)
            if insert_donor(conn, donor):
                print("Donor added successfully.")
            print("Press Enter to return to the main menu...")
            input()

        elif choice == '5':
            donar_info_view(conn)

        elif choice == '6':
            print("Emergency Blood Request feature is under development.")
            while True:
                request_blood_type = input("Enter required blood type: ")
                if request_blood_type in BLOOD_TYPES:
                    break
                else:
                    print("Invalid blood type. Please enter a valid blood type.")

            # Here you can add code to handle emergency blood requests, such as prioritizing donors with urgent availability
            print("Press Enter to return to the main menu...")
            input()

        elif choice == '7':
            settings_view(conn, current_user)

        elif choice == '8':
            print("Logging out...")
            sleep(3)
            default_view(conn)
            break

        elif choice == '9':
            print("Exiting the system. Goodbye!")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")


def donar_info_view(conn):
    """ Display donor information in a tabular format """
    donar_info = get_all_donors_info(conn)
    print("Donor Information:")
    print("+----+----------------+----------------+----------------+----------------+----------------+----------------+----------------+")
    print("| DID | Name           | Phone          | Address        | DoB            | Gender         | Blood Type     | Last Donation Date |")
    print("+----+----------------+----------------+----------------+----------------+----------------+----------------+----------------+")
    for donor in donar_info:
        print(f"| {donor[0]:<4} | {donor[1]:<14} | {donor[2]:<14} | {donor[3]:<14} | {donor[4]:<14} | {donor[5]:<14} | {donor[6]:<14} | {donor[7]:<16} |")
    print("+----+----------------+----------------+----------------+----------------+----------------+----------------+----------------+")
    print("1. Update Donor Information")
    print("Press Q to return to the main menu...")
    input()


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
            if not login_user(conn, current_user, hash_password(current_password)):
                print("Incorrect current password. Please try again.")
                continue
            new_password = getpass.getpass(prompt="Enter new password: ").strip()
            if not is_strong_password(new_password):
                print("Password must be at least 8 characters long and include uppercase letters, lowercase letters, and numbers.")
                continue
            # Code to update the user's password in the database
            change_user_password(conn, current_user, hash_password(new_password))
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


def available_units_view(conn):
    """ Display available blood units in a tabular format """
    available_units = get_available_blood_units(conn)
    print("Available Blood Units:")
    print("+------------+-----------------+")
    print("| Blood Type | Available Units |")
    print("+------------+-----------------+")
    for blood_type, units in available_units:
        print(f"| {blood_type:<10} | {units:>15} |")
    print("+------------+-----------------+")
    print("Press Enter to return to the main menu...")
    input()


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
        user = User(name, username, hash_password(password))
        insert_user(conn, user)
        print("User created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")


def update_blood_donation_usage(conn, blood_type, units_requested=1):
    """ Update the status of a blood donation record to used """
    blood_units = get_blood_types_donation_by_id(conn, blood_type)

    try:
        while blood_units and units_requested > 0:
            bid, available_units = blood_units[0]

            if available_units <= units_requested:
                update_blood_donation_by_id(conn, bid, is_used=True)
                units_requested -= available_units
                blood_units.pop(0)
            else:
                update_blood_donation_by_id(conn, bid, is_used=False, units_used=units_requested)
                units_requested = 0
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error updating blood donation usage: {e}")


if __name__ == "__main__":
    main()
