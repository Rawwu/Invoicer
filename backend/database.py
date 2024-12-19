# SQLite database setup

import sqlite3

# Initialize the database connection
def get_db_connection():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Create necessary tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time_spent REAL,
            labor_cost REAL,
            gas_expenses REAL,
            additional_charges REAL,
            total_cost REAL
        )
    ''')

    conn.commit()
    conn.close()

# Insert job data into the database
def save_job(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO jobs (name, date, time_spent, labor_cost, gas_expenses, additional_charges, total_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['date'],
        data['time_spent'],
        data['labor_cost'],  # Update column name here
        data['gas_expenses'],
        data['additional_charges'],
        data['total_cost']
    ))

    conn.commit()
    conn.close()

def get_all_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, date, time_spent, labor_cost, gas_expenses, additional_charges, total_cost FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    # Include the name column
    columns = ["name", "date", "time_spent", "labor_cost", "gas_expenses", "additional_charges", "total_cost"]
    jobs_dict = [dict(zip(columns, job)) for job in jobs]
    return jobs_dict
