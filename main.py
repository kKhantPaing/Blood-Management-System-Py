""" Main application file for the Blood Management System """
import sqlite3
import os
import sys
import getpass
import string
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
    update_blood_donation_by_id,
    update_donor_info,
    get_blood_type_by_donor_id,
    get_compatible_blood_types,
    get_blood_units_by_compatible_types,
    get_donor_info
)
from models import Donor, User
from utils import hash_password


DB_NAME = "blood_management.db"  # DB Name

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]  # Blood Types


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

        if choice == '1':  # Login
            username = input("Enter your username: ").lower()
            password = getpass.getpass(prompt="Enter your password: ").strip()
            current_user = login_user(conn, username, hash_password(password))

            if current_user:  # Display user-specific options here
                auth_user_view(conn, current_user)
                break
            else:
                print("Invalid credentials. Please try again.")

        elif choice == '2':  # View Available Blood Units
            available_units_view(conn)

        elif choice == '3':  # Exit
            print("Exiting the system. Goodbye!")
            sys.exit()

        else:  # Invalid choice
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

        if choice == '1':  # View Available Blood Units
            available_units_view(conn)

        elif choice == '2':  # Request Blood Units by Blood Type
            print("Request Blood Units by Blood Type: \n")

            blood_type = get_valid_blood_type("Enter required blood type: ", BLOOD_TYPES)

            units = get_valid_units(f"Enter number of units for {blood_type}: ")

            available_units = get_blood_units_by_type(conn, blood_type)

            if available_units >= units:
                update_blood_donation_usage(conn, blood_type, units)
                print(f"Request successful! {units} units of {blood_type} blood have been allocated to you.")
            else:
                print(f"Sorry, only {available_units} units of {blood_type} blood are available. Your request cannot be fulfilled.")
                while True:
                    print("Do you want to use them? (yes/no)")
                    use_available = input().strip().lower()
                    if use_available == 'yes':
                        update_blood_donation_usage(conn, blood_type, available_units)
                        print(f"Request successful! {available_units} units of {blood_type} blood have been allocated to you.")
                        break
                    elif use_available == 'no':
                        print("Request cancelled. Returning to main menu.")
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")

                pause_and_return()

        elif choice == '3':  # Add New Blood Unit
            while True:
                donor_id = input("Enter donor ID (or type 'cancel' to go back): ")

                if donor_id.lower() == 'cancel':
                    return

                blood_type = get_blood_type_by_donor_id(conn, donor_id)  # Check if donor ID exists and get blood type
                if blood_type:
                    print(f"Blood type for donor ID {donor_id} is {blood_type}.")
                    break
                else:
                    print("Invalid donor ID. Please enter a valid donor ID.")

            units = get_valid_units(f"Enter number of units for {blood_type}: ")

            donation_date = get_valid_date("Enter donation date (YYYY-MM-DD): ")
            expiration_date = datetime.strptime(donation_date, "%Y-%m-%d") + timedelta(days=42)  # Blood typically expires after 42 days

            blood_donation = (donor_id, blood_type, units, donation_date, expiration_date)

            if insert_blood_donation(conn, blood_donation):
                print("Blood donation added successfully.")

            pause_and_return()

        elif choice == '4':  # Add New Donor
            donor_name = input("Enter donor's name: ")
            donor_phone = get_valid_phone("Enter donor's phone number: ")
            donor_address = input("Enter donor's address: ")
            donor_dob = get_valid_date("Enter donor's date of birth (YYYY-MM-DD): ")
            donor_gender = get_valid_gender("Enter donor's gender (Male/Female/Other): ")
            donor_blood_type = get_valid_blood_type("Enter donor's blood type: ", BLOOD_TYPES)

            last_donation_date = get_valid_date("Enter last donation date (YYYY-MM-DD) or leave blank if never donated: ", is_required=False)
            is_urgent_available = input("Is the donor urgently available? (yes/no): ").strip().lower() == 'yes'

            donor = (donor_name, donor_phone, donor_address, donor_dob, donor_gender, donor_blood_type,
                     last_donation_date, is_urgent_available)

            insert_donor(conn, donor)

            pause_and_return()

        elif choice == '5':  # View Donor Information
            donor_info_view(conn)

        elif choice == '6':  # Emergency Blood Request
            print("Emergency Blood Request")
            request_blood_type = get_valid_blood_type("Enter required blood type: ", BLOOD_TYPES)

            compatible_blood_types = get_compatible_blood_types(conn, request_blood_type)

            if compatible_blood_types:

                while True:

                    print(f"Compatible blood types for {request_blood_type}: {', '.join(compatible_blood_types)}")
                    compatible_blood_units = get_blood_units_by_compatible_types(conn, compatible_blood_types)
                    print("+------------+-----------------+")
                    print("| Blood Type | Available Units |")
                    print("+------------+-----------------+")
                    for blood_type, units in compatible_blood_units:
                        print(f"| {blood_type:<10} | {units:>15} |")
                    print("+------------+-----------------+\n")

                    print("1. Request Blood Units by Compatible Blood Types")
                    print("2. Request Donors with Urgent Availability for Compatible Blood Types")
                    print("Press B to return to the main menu...")
                    choice = input("Enter your choice: ").strip().lower()

                    if choice == 'b':
                        print("Returning to main menu...")
                        sleep(2)
                        auth_user_view(conn, current_user)
                        return

                    if choice == '1':
                        blood_type = get_valid_blood_type("Enter blood type to request: ", compatible_blood_types)
                        units = get_valid_units(f"Enter number of units for {blood_type}: ")

                        units_dict = dict(compatible_blood_units)
                        available_units = units_dict.get(blood_type, 0)

                        if available_units >= units:
                            update_blood_donation_usage(conn, blood_type, units)
                            print(f"Request successful! {units} units of {blood_type} blood have been allocated to you.\n\n")

                        else:
                            print(f"Sorry, only {available_units} units of {blood_type} blood are available. Your request cannot be fulfilled.")

                    elif choice == '2':
                        print("Donors with urgent availability for compatible blood types feature is under development.")

        elif choice == '7':  # Settings
            settings_view(conn, current_user)

        elif choice == '8':  # Logout
            print("Logging out...")
            sleep(3)
            default_view(conn)
            break

        elif choice == '9':  # Exit
            print("Exiting the system. Goodbye!")
            sys.exit()

        else:  # Invalid choice
            print("Invalid choice. Please try again.")


def donor_info_view(conn):
    """ Display donor information in a tabular format """
    donor_info = get_all_donors_info(conn)
    print("Donor Information:")
    print("+----+----------------+----------------+----------------+----------------+----------------+----------------+----------------+")
    print("| DID | Name           | Phone          | Address        | DoB            | Gender         | Blood Type     | Last Donation Date |")
    print("+----+----------------+----------------+----------------+----------------+----------------+----------------+----------------+")
    for donor in donor_info:
        print(f"| {donor[0]:<4} | {donor[1]:<14} | {donor[2]:<14} | {donor[3]:<14} | {donor[4]:<14} | {donor[5]:<14} | {donor[6]:<14} | {donor[7]:<16} |")
    print("+----+----------------+----------------+----------------+----------------+----------------+----------------+----------------+")

    print("1. Update Donor Information")
    print("B. Back to Main Menu")
    choice = input("Enter your choice: ").strip().lower()

    if choice == '1':
        while True:
            result = get_donor_info(conn, input("Enter Donar ID to update: "))
            if result is not None:
                break
            print("Invalid Donar Id")
        print(f"Name: {result[0]}")
        print(f"Phone: {result[1]}")
        print(f"Address: {result[2]}")
        print(f"Date of Birth: {result[3]}")
        print(f"Gender: {result[4]}")
        print(f"Blood Type: {result[5]}")
        print(f"Last Donation Date: {result[6]}")
        print(f"Urgent Availability: {'Yes' if result[7] else 'No'}")
        print("\nEnter new information (leave blank to keep current value):")

        new_phone = get_valid_phone("Phone: ") or result[1]
        new_address = input("Address: ").strip() or result[2]
        new_last_donation_date = get_valid_date("Last Donation Date (YYYY-MM-DD): ", is_required=False) or result[6]
        new_urgent_availability = input("Is the donor urgently available? (yes/no): ").strip().lower()

        # Code to update the donor information in the database
        donor_info = Donor(
            donor_id=choice,
            name=result[0],
            phone=new_phone,
            address=new_address,
            dob=result[3],
            gender=result[4],
            blood_type=result[5],
            last_donation_date=new_last_donation_date,
            is_urgent_available=(new_urgent_availability == 'yes')
        )
        update_donor_info(conn, donor_info)

    else:
        print("Invalid choice.")
        print("Returning to main menu...")
        sleep(2)
        pause_and_return(is_directly_return=True)


def settings_view(conn, current_user):
    """ Display settings view for the current user """
    while True:
        print(f"Settings for {current_user}:")
        print("\nMenu:")
        print("1. Change Password")
        print("2. Add New User")
        print("3. Reset Database")
        print("B. Back to Main Menu")
        choice = input("Enter your choice: ").strip().lower()

        clear_screen()

        if choice == '1':  # Change Password
            current_password = getpass.getpass(prompt="Enter your current password: ").strip()
            if not login_user(conn, current_user, hash_password(current_password)):
                print("Incorrect current password. Please try again.")
                continue

            new_password = get_valid_password()

            # Code to update the user's password in the database
            change_user_password(conn, current_user, hash_password(new_password))

        elif choice == '2':  # Add New User
            add_new_user(conn)

        elif choice == '3':  # Reset Database
            confirm = input("Are you sure you want to reset the database? This action cannot be undone. (yes/no): ")

            if confirm.lower() == 'yes':
                reset_database(conn)
                print("Database has been reset. Returning to database setup.")
                first_time_setup(conn)
                break
            else:
                print("Database reset cancelled.")
        elif choice == 'b':
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

    pause_and_return()


def clear_screen():
    """ Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def add_new_user(conn):
    """ Add a new user to the system """
    name = input("Enter user's name: ")
    username = input("Enter username: ").strip().lower()

    if is_username_exists(conn, username):
        print("Username already exists. Please choose a different username.")
        return

    password = get_valid_password()

    user = User(name, username, hash_password(password))
    insert_user(conn, user)


def pause_and_return(is_directly_return=False):
    """ Pause the program and wait for user input to return to the main menu """
    if not is_directly_return:
        input("\nPress Enter to return to the main menu...")


def update_blood_donation_usage(conn, blood_type, units_requested=1):
    """ Update the status of a blood donation record to used """
    blood_units = get_blood_types_donation_by_id(conn, blood_type)

    try:
        for bid, available_units in blood_units:

            if units_requested <= 0:
                break

            if available_units <= units_requested:
                update_blood_donation_by_id(conn, bid, is_used=True)
                units_requested -= available_units

            else:
                update_blood_donation_by_id(conn, bid, is_used=False, units_used=units_requested)
                units_requested = 0

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error updating blood donation usage: {e}")


def get_valid_blood_type(prompt, valid_types) -> str:
    """ Get a valid blood type input from the user """
    while True:
        blood_type = input(prompt).strip().upper()
        if blood_type in valid_types:
            return blood_type
        print("Invalid blood type. Please enter a valid one.")


def get_valid_units(prompt: str) -> int:
    """ Get a valid units input from the user """
    while True:
        try:
            units = int(input(prompt).strip())
            if units >= 0:
                return units
            print("Units cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_valid_date(prompt: str, is_required: bool = True) -> str:
    """ Get a valid date in YYYY-MM-DD format from the user """
    while True:
        date_str = input(prompt).strip()

        if not is_required and not date_str:
            return ""

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format (e.g., 2000-12-31).")


def get_valid_phone(prompt: str) -> str:
    """ Get a valid phone number input from the user """
    while True:
        phone = input(prompt).strip()
        if phone.isdigit() and 7 <= len(phone) <= 15:
            return phone
        print("Invalid phone number. Please enter digits only (7–15 digits).")


def get_valid_gender(prompt: str) -> str:
    """ Get a valid gender input from the user """
    while True:
        gender = input(prompt).strip().capitalize()
        if gender in ["Male", "Female", "Other"]:
            return gender
        print("Invalid input. Please enter Male, Female, or Other.")


def get_valid_password() -> str:
    """ Get a valid password input from the user that meets strength requirements """
    special_chars = string.punctuation

    while True:
        password = getpass.getpass(prompt="Enter password: ").strip()

        if not (8 <= len(password) <= 32):
            print("Password must be between 8 and 32 characters long.")
            continue
        if not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
            continue
        if not any(char.islower() for char in password):
            print("Password must contain at least one lowercase letter.")
            continue
        if not any(char.isdigit() for char in password):
            print("Password must contain at least one digit.")
            continue
        if not any(char in special_chars for char in password):
            print("Password must contain at least one special character.")
            continue

        confirm_password = getpass.getpass(prompt="Confirm password: ").strip()
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue

        return password


if __name__ == "__main__":
    main()
