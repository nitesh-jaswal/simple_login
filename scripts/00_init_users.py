import sqlite3

# Path to your SQLite database file
DATABASE_FILE = "database.db"

# SQL statement to create the users table
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
"""

def init_db():
    # Connect to the SQLite database. This will create the file if it doesn't exist.
    conn = sqlite3.connect(DATABASE_FILE)
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute the SQL statement to create the table
    cursor.execute(CREATE_USERS_TABLE)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
