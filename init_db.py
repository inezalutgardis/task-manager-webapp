import sqlite3

# How I connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# I created a tasks table below
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
''')

conn.commit()
conn.close()

print("Database initialized! ✅")
