""" Database operations for the Blood Management System """
import sqlite3
from utils import hash_password


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    
    return conn


def create_tables(conn):
    """ create tables in the SQLite database """

    create_user_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                    UID integer PRIMARY KEY,
                                    Name text NOT NULL,
                                    Username text NOT NULL,
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
                                    is_available integer NOT NULL DEFAULT 1
                                ); """
    
    create_blood_relationship_table_sql = """ CREATE TABLE IF NOT EXISTS blood_relationships (
                                    Main_Blood_Type text NOT NULL CHECK(Main_Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                                    Compatible_Blood_type text NOT NULL CHECK(Compatible_Blood_type != Main_Blood_Type AND Compatible_Blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
                                ); """
    
    create_setting_table_sql = """ CREATE TABLE IF NOT EXISTS settings (
                                    SID integer PRIMARY KEY,
                                    Key text NOT NULL,
                                    Value text NOT NULL
                                ); """
    
    create_blood_donation_table_sql = """ CREATE TABLE IF NOT EXISTS blood_donations (
                                    BDID integer PRIMARY KEY,
                                    Donor_ID integer NOT NULL,
                                    Blood_Type text NOT NULL CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                                    Donation_Date text NOT NULL,
                                    Expiration_Date text NOT NULL,
                                    FOREIGN KEY (Donor_ID) REFERENCES donors (DID)
                                ); """
    
    try:
        create_table(conn, create_user_table_sql)
        create_table(conn, create_donor_table_sql)
        create_table(conn, create_blood_relationship_table_sql)
        create_table(conn, create_setting_table_sql)
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


def insert_donor(conn, donor):
    """ Insert a new donor into the donors table """
    sql = ''' INSERT INTO donors(name, phone, address, blood_type, is_available)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, donor)
    conn.commit()
    return cur.lastrowid        


def get_donor_by_id(conn, donor_id):
    """ Query donors by id """
    cur = conn.cursor()
    cur.execute("SELECT * FROM donors WHERE DID=?", (donor_id,))
    row = cur.fetchone()
    return row


def get_all_donors(conn):
    """ Query all donors """
    cur = conn.cursor()
    cur.execute("SELECT * FROM donors")
    rows = cur.fetchall()
    return rows


def update_donor_availability(conn, donor_id, is_available):
    """ Update donor availability status """
    sql = ''' UPDATE donors
              SET is_available = ?
              WHERE DID = ? '''
    cur = conn.cursor()
    cur.execute(sql, (is_available, donor_id))
    conn.commit()


def get_available_donors_by_blood_type(conn, blood_type):
    """ Query available donors by blood type """
    cur = conn.cursor()
    cur.execute("SELECT * FROM donors WHERE Blood_Type=? AND is_available=1", (blood_type,))
    rows = cur.fetchall()
    return rows


def get_compatible_blood_types_donor(conn, blood_type):
    """ Query compatible blood types for a given blood type """
    cur = conn.cursor()
    cur.execute("SELECT Compatible_Blood_type FROM blood_relationships WHERE Main_Blood_Type=?", (blood_type,))
    rows = cur.fetchall()
    return [row[0] for row in rows]


def insert_blood_type(conn, blood_type):
    """ Insert a new blood type into the blood_types table """
    sql = ''' INSERT INTO blood_types(blood_type, rh, description)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, blood_type)
    conn.commit()
    return cur.lastrowid


def insert_user(conn, user):
    """ Insert a new user into the users table """
    user = (user.name, user.username, hash_password(user.password))
    sql = ''' INSERT INTO users(Name, Username, Password)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def login_user(conn, username, password):
    """ Authenticate a user by username and password """
    hashed_password = hash_password(password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE Username=? AND Password=?", (username, hashed_password))
    row = cur.fetchone()
    return True if row else False


def get_blood_availability(conn):
    """ Query blood availability """
    sql = ''' SELECT bt.Blood_Type,
       COALESCE(a.Available_Count, 0) AS Available_Count
        FROM (
            SELECT 'A+' AS Blood_Type UNION ALL
            SELECT 'A-' UNION ALL
            SELECT 'B+' UNION ALL
            SELECT 'B-' UNION ALL
            SELECT 'AB+' UNION ALL
            SELECT 'AB-' UNION ALL
            SELECT 'O+' UNION ALL
            SELECT 'O-'
        ) bt
        LEFT JOIN (
            SELECT Blood_Type, COUNT(*) AS Available_Count
            FROM blood_donations
            WHERE Donation_Date <= date('now')
            AND Expiration_Date >= date('now')
            GROUP BY Blood_Type
        ) tmp
        ON tmp.Blood_Type = bt.Blood_Type
        ORDER BY bt.Blood_Type;
        '''

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows
