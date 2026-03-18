""" Database operations for the Blood Management System """
import sqlite3

BLOOD_RELATION_DATA = [
    ("A+", "A-"), ("A+", "O+"), ("A+", "O-"),
    ("A-", "O-"),
    ("B+", "B-"), ("B+", "O+"), ("B+", "O-"),
    ("B-", "O-"),
    ("AB+", "AB-"), ("AB+", "A+"), ("AB+", "A-"),
    ("AB+", "B+"), ("AB+", "B-"), ("AB+", "O+"), ("AB+", "O-"),
    ("AB-", "A-"), ("AB-", "B-"), ("AB-", "O-"),
    ("O+", "O-"),
]


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")

    return conn


def setup_database(conn):
    """ Set up the database by creating tables and inserting default data """
    try:
        define_tables(conn)
        insert_default_blood_relationships(conn)
        print("Database setup successful")
    except sqlite3.Error as e:
        print(f"Error setting up database: {e}")


def reset_database(conn):
    """ Reset the database by dropping all tables and recreating them """
    try:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS users")
        c.execute("DROP TABLE IF EXISTS donors")
        c.execute("DROP TABLE IF EXISTS blood_relationships")
        c.execute("DROP TABLE IF EXISTS blood_donations")
        print("Database reset successful")
        setup_database(conn)
    except sqlite3.Error as e:
        print(f"Error resetting database: {e}")


def define_tables(conn):
    """ create tables in the SQLite database """

    create_user_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                    UID integer PRIMARY KEY,
                                    Name text NOT NULL,
                                    Username text NOT NULL UNIQUE,
                                    Password text NOT NULL
                                ); """

    create_donor_table_sql = """ CREATE TABLE IF NOT EXISTS donors (
                                    DID integer PRIMARY KEY,
                                    Name text NOT NULL,
                                    Phone text NOT NULL,
                                    Address text NOT NULL,
                                    DoB text NOT NULL,
                                    Gender text NOT NULL,
                                    Blood_Type text NOT NULL CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                                    Last_Donation_Date TEXT,
                                    is_urgent_available integer NOT NULL DEFAULT 1,
                                    is_deleted integer NOT NULL DEFAULT 0
                                ); """

    create_blood_relationship_table_sql = """ CREATE TABLE IF NOT EXISTS blood_relationships (
                                    Main_Blood_Type text NOT NULL CHECK(Main_Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                                    Compatible_Blood_type text NOT NULL CHECK(Compatible_Blood_type != Main_Blood_Type AND Compatible_Blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
                                ); """

    create_blood_donation_table_sql = """ CREATE TABLE IF NOT EXISTS blood_donations (
                                    BDID integer PRIMARY KEY,
                                    Donor_ID integer NOT NULL,
                                    Blood_Type text NOT NULL CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                                    Units integer NOT NULL,
                                    Donation_Date text NOT NULL,
                                    Status text NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'used', 'expired')),
                                    Expiration_Date text NOT NULL,
                                    FOREIGN KEY (Donor_ID) REFERENCES donors (DID)
                                ); """

    try:
        create_table(conn, create_user_table_sql)
        create_table(conn, create_donor_table_sql)
        create_table(conn, create_blood_relationship_table_sql)
        create_table(conn, create_blood_donation_table_sql)
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")


def insert_default_blood_relationships(conn):
    """ Insert default blood compatibility relations into the blood_relationships table """
    sql = ''' INSERT INTO blood_relationships(Main_Blood_Type, Compatible_Blood_type)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, BLOOD_RELATION_DATA)
    conn.commit()


def insert_user(conn, user):
    """ Insert a new user into the users table """
    name, username, password = (user.name, user.username.lower(),
                                user.password)
    sql = ''' INSERT INTO users(Name, Username, Password) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, username, password))
    conn.commit()
    print(f"User {name} inserted successfully with ID: {cur.lastrowid}")
    return cur.lastrowid


def insert_donor(conn, donor):
    """ Insert a new donor into the donors table """
    sql = ''' INSERT INTO donors(name, phone, address, dob, gender, blood_type,
                Last_Donation_Date, is_urgent_available, is_deleted)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, donor)
    conn.commit()
    return cur.lastrowid


def insert_blood_donation(conn, blood_donation):
    """ Insert a new blood donation record into the blood_donations table """
    try:
        sql = ''' INSERT INTO blood_donations(Donor_ID, Blood_Type, Units,
                    Donation_Date, Expiration_Date)
                  VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, blood_donation)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting blood donation: {e}")
        return None


def is_username_exists(conn, username):
    """Check whether a username already exists in the users table."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM users WHERE Username=? LIMIT 1", (username.lower(),))
    except sqlite3.Error as e:
        print(f"Error checking username: {e}")
        return False
    return cur.fetchone() is not None


def login_user(conn, username, password):
    """ Authenticate a user by username and password """
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM users WHERE Username=? AND Password=? LIMIT 1",
                    (username.lower(), password))
    except sqlite3.Error as e:
        print(f"Error during login: {e}")
        return False
    return username if cur.fetchone() is not None else ""


def change_user_password(conn, username, new_password):
    """ Change the password for a given username """
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET Password=? WHERE Username=?",
                    (new_password, username.lower()))
        conn.commit()
        print("Password updated successfully")
    except sqlite3.Error as e:
        print(f"Error changing password: {e}")


def update_blood_donation_status(conn, expired_date):
    """ Update the status of a blood donation record """
    cur = conn.cursor()
    try:
        cur.execute("UPDATE blood_donations SET Status=? WHERE Expiration_Date<?",
                    ("expired", expired_date))
        conn.commit()
        print(f"Blood donation status updated to expired for records with expiration date before {expired_date}")
    except sqlite3.Error as e:
        print(f"Error updating blood donation status: {e}")


def get_available_blood_units(conn):
    """ Retrieve available blood units for all blood types, showing 0 when none exist """
    cur = conn.cursor()
    try:
        cur.execute("""
            WITH all_blood_types(Blood_Type) AS (
            VALUES ('A+'), ('A-'), ('B+'), ('B-'), ('AB+'), ('AB-'), ('O+'), ('O-')
            ),
            available_units AS (
                SELECT Blood_Type, SUM(Units) AS Total_Units
                FROM blood_donations
                WHERE Expiration_Date > date('now')
                AND Status = 'available'
                GROUP BY Blood_Type
            )
            SELECT t.Blood_Type, COALESCE(a.Total_Units, 0) AS Total_Units
            FROM all_blood_types t
            LEFT JOIN available_units a USING (Blood_Type)
            ORDER BY CASE t.Blood_Type
                WHEN 'A+' THEN 1 WHEN 'A-' THEN 2
                WHEN 'B+' THEN 3 WHEN 'B-' THEN 4
                WHEN 'AB+' THEN 5 WHEN 'AB-' THEN 6
                WHEN 'O+' THEN 7 WHEN 'O-' THEN 8
            END;
        """)
    except sqlite3.Error as e:
        print(f"Error retrieving blood units: {e}")
        return []
    return cur.fetchall()


def get_all_donors_info(conn):
    """ Retrieve all donor information from the donors table """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM donors WHERE is_deleted=0")
    except sqlite3.Error as e:
        print(f"Error retrieving donors info: {e}")
        return []
    return cur.fetchall()


def get_donor_info(conn, donor_id):
    """ Retrieve donor information by donor ID """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM donors WHERE DID=?", (donor_id,))
    except sqlite3.Error as e:
        print(f"Error retrieving donor info: {e}")
        return None
    return cur.fetchone()