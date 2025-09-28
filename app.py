import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

# Below I create the Flask application
app = Flask(__name__)

# The code below ensures that the database exists (important for Render)
if not os.path.exists("tasks.db"):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT NOT NULL,
                  done BOOLEAN NOT NULL CHECK (done IN (0,1)))''')
    conn.commit()
    conn.close()

# Below is a database helper function that helps me talk to tasks.db easily.
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row  # Makes rows behave like dictionaries
    return conn

# Home route: this shows the list of tasks
@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# How I add a new task to the database
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")  # How I get a task from form
    print("DEBUG: Task received from form:", task)  # Debug line

    if task:
        conn = get_db_connection()
        # I wanted to prevent duplicates (ignore case and extra spaces)
        existing = conn.execute(
            "SELECT * FROM tasks WHERE lower(content) = ?",
            (task.lower().strip(),)
        ).fetchone()

        if not existing:
            conn.execute(
                "INSERT INTO tasks (content, done) VALUES (?, ?)",
                (task.strip(), 0)
            )
            conn.commit()
        conn.close()

    return redirect(url_for("index"))

# How I mark a task as complete
@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# How I delete a task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Finally, how I run the app
if __name__ == "__main__":
    app.run(debug=True, port=5001)