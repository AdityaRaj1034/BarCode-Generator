import sqlite3

# Connect to SQLite database (this will create a new database if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create User table
cursor.execute('''
    DELETE FROM users;
''')

# Commit changes and close the connection
conn.commit()
conn.close()


