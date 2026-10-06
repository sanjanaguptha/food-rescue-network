import sqlite3


# ==============================
# CREATE DATABASE
# ==============================

def create_database():

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    # Donors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT
        )
    """)

    # Donations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            size TEXT,
            description TEXT,
            condition TEXT,
            status TEXT DEFAULT 'REGISTERED',
            delivery_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Delivery persons table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS delivery_persons (
            delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            available INTEGER DEFAULT 1
        )
    """)

    # Add delivery_id to old database if missing
    cursor.execute("PRAGMA table_info(donations)")
    columns = [column[1] for column in cursor.fetchall()]

    if "delivery_id" not in columns:
        cursor.execute("""
            ALTER TABLE donations
            ADD COLUMN delivery_id INTEGER
        """)

    connection.commit()
    connection.close()


# ==============================
# ADD DONOR
# ==============================

def add_donor(name, phone, address, email):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO donors
        (name, phone, address, email)
        VALUES (?, ?, ?, ?)
    """, (name, phone, address, email))

    donor_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return donor_id


# ==============================
# ADD DONATION
# ==============================

def add_donation(
    donor_id,
    category,
    item_name,
    quantity,
    size,
    description,
    condition
):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO donations
        (
            donor_id,
            category,
            item_name,
            quantity,
            size,
            description,
            condition
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        donor_id,
        category,
        item_name,
        quantity,
        size,
        description,
        condition
    ))

    donation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return donation_id


# ==============================
# ADD DELIVERY PERSON
# ==============================

def add_delivery_person(name, phone, address):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO delivery_persons
        (name, phone, address)
        VALUES (?, ?, ?)
    """, (name, phone, address))

    delivery_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return delivery_id


# ==============================
# GET DELIVERY PERSONS
# ==============================

def get_delivery_persons():

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT delivery_id, name, phone
        FROM delivery_persons
        WHERE available = 1
    """)

    delivery_persons = cursor.fetchall()

    connection.close()

    return delivery_persons


# ==============================
# ASSIGN DELIVERY PERSON
# ==============================

def assign_delivery_person(donation_id, delivery_id):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE donations
        SET delivery_id = ?,
            status = 'ASSIGNED'
        WHERE donation_id = ?
    """, (delivery_id, donation_id))

    connection.commit()
    connection.close()


# ==============================
# UPDATE DONATION STATUS
# ==============================

def update_donation_status(donation_id, status):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE donations
        SET status = ?
        WHERE donation_id = ?
    """, (status, donation_id))

    connection.commit()
    connection.close()


# ==============================
# GET DONATION DETAILS
# ==============================

def get_donation_details(donation_id):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            d.donation_id,
            d.category,
            d.item_name,
            d.quantity,
            d.size,
            d.description,
            d.condition,
            d.status,

            donors.name,
            donors.phone,
            donors.address,

            delivery_persons.name,
            delivery_persons.phone

        FROM donations d

        JOIN donors
        ON d.donor_id = donors.donor_id

        LEFT JOIN delivery_persons
        ON d.delivery_id = delivery_persons.delivery_id

        WHERE d.donation_id = ?
    """, (donation_id,))

    donation = cursor.fetchone()

    connection.close()

    return donation
# ==============================
# ADMIN DASHBOARD
# ==============================

# ==============================
# ADMIN STATISTICS
# ==============================

def get_admin_statistics():

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    # Total donors
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    # Total donations
    cursor.execute("SELECT COUNT(*) FROM donations")
    total_donations = cursor.fetchone()[0]

    # Total delivery persons
    cursor.execute("SELECT COUNT(*) FROM delivery_persons")
    total_delivery_persons = cursor.fetchone()[0]

    # Get status counts
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM donations
        GROUP BY status
    """)

    database_status_counts = dict(cursor.fetchall())

    # Always show all statuses
    statuses = [
        "REGISTERED",
        "ASSIGNED",
        "PICKED UP",
        "OUT FOR DELIVERY",
        "DELIVERED"
    ]

    status_counts = []

    for status in statuses:

        count = database_status_counts.get(status, 0)

        status_counts.append(
            (status, count)
        )

    connection.close()

    return (
        total_donors,
        total_donations,
        total_delivery_persons,
        status_counts
    )
# ==============================
# RECORD DISTRIBUTION
# ==============================

def record_distribution(donation_id, recipient_name, location):

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS distributions (
            distribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER NOT NULL,
            recipient_name TEXT NOT NULL,
            location TEXT NOT NULL,
            distributed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO distributions
        (donation_id, recipient_name, location)
        VALUES (?, ?, ?)
    """, (
        donation_id,
        recipient_name,
        location
    ))

    connection.commit()
    connection.close()
# ==============================
# ADMIN DASHBOARD - CATEGORY STATS
# ==============================

# ==============================
# CATEGORY STATISTICS
# ==============================

def get_category_statistics():

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM donations
        GROUP BY category
    """)

    database_categories = dict(cursor.fetchall())

    # Always show all categories
    categories = [
        "Food",
        "Clothes",
        "Other"
    ]

    category_counts = []

    for category in categories:

        count = database_categories.get(
            category,
            0
        )

        category_counts.append(
            (category, count)
        )

    connection.close()

    return category_counts


# ==============================
# ADMIN DASHBOARD - DELIVERED
# ==============================

def get_delivered_count():

    connection = sqlite3.connect("food_rescue.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM donations
        WHERE status = 'DELIVERED'
    """)

    delivered_count = cursor.fetchone()[0]

    connection.close()

    return delivered_count
