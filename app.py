import sqlite3
from flask import Flask, jsonify, render_template, request, redirect, session,flash
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.secret_key = "super_secret_key"


# ---------------- DATABASE CONNECTION ---------------- #

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE DATABASE ---------------- #

@app.route("/create_db")
def create_db():
    conn = get_db_connection()

    # ---------------- Users ---------------- #
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ---------------- Parent ---------------- #
    conn.execute("""
    CREATE TABLE IF NOT EXISTS parent (
        parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        phone TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # ---------------- Child ---------------- #
    conn.execute("""
    CREATE TABLE IF NOT EXISTS child (
        child_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        parent_id INTEGER,
        name TEXT,
        class_name TEXT,
        student_type TEXT,
        FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # ---------------- Tasks ---------------- #
    conn.execute("""     
    CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER,
    task_name TEXT,
    assigned_by TEXT,
    due_date TEXT
)
""")
# ---------------- Child Task Status ---------------- #
    conn.execute("""
    CREATE TABLE IF NOT EXISTS child_task_status(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    child_id INTEGER,
    completed INTEGER DEFAULT 0,
    proof_image TEXT,
    completed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
    
 
    conn.execute("""
    CREATE TABLE IF NOT EXISTS app_usage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER,
        app_name TEXT,
        usage_time INTEGER,
        date TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER,
        parent_message TEXT,
        child_message TEXT,
        created_at TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS app_restrictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER,
        app_name TEXT,
        time_limit INTEGER
    )
    """)

    conn.commit()
    conn.close()

    return "✅ Database Ready!"

# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Parent data
        pname = request.form["parent_name"]
        parent_email = request.form["email"]
        parent_password = request.form["parent_password"]
        phone = request.form["phone"]

        # Child data
        cname = request.form["child_name"]
        child_email = request.form["child_email"]
        child_password = request.form["child_password"]
        class_name = request.form["class"]
        student_type = request.form["student_type"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Insert Parent into users
        cursor.execute("""
            INSERT INTO users (fullname, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (pname, parent_email, parent_password, "parent"))

        parent_user_id = cursor.lastrowid

        # 2️⃣ Insert into parent table
        cursor.execute("""
            INSERT INTO parent (user_id, phone)
            VALUES (?, ?)
        """, (parent_user_id, phone))

        parent_id = cursor.lastrowid

        # 3️⃣ Insert Child into users
        cursor.execute("""
            INSERT INTO users (fullname, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (cname, child_email, child_password, "child"))

        child_user_id = cursor.lastrowid

        # 4️⃣ Insert into child table
        cursor.execute("""
            INSERT INTO child (user_id, parent_id, name, class_name, student_type)
            VALUES (?, ?, ?, ?, ?)
        """, (child_user_id, parent_id, cname, class_name, student_type))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute("""
            SELECT * FROM users WHERE email=? AND password=?
        """, (email, password)).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["fullname"] = user["fullname"]

            if user["role"] == "parent":
                return redirect("/parent_dashboard")
            else:
                return redirect("/child_dashboard")

        return render_template("login.html", message="Invalid credentials!")

    return render_template("login.html")


# ---------------- PARENT DASHBOARD ---------------- #

@app.route("/parent_dashboard")
def parent_dashboard():

    if session.get("role") != "parent":
        return redirect("/")

    conn = get_db_connection()

    # Get parent_id
    parent = conn.execute("""
        SELECT parent_id FROM parent WHERE user_id=?
    """, (session["user_id"],)).fetchone()

    # Get children of this parent
    children = conn.execute("""
        SELECT * FROM child WHERE parent_id=?
    """, (parent["parent_id"],)).fetchall()

    conn.close()

    return render_template("parent_dashboard.html",
                           children=children,
                           fullname=session["fullname"])


# ---------------- CHILD DASHBOARD ---------------- #

@app.route("/child_dashboard")
def child_dashboard():

    if session.get("role") != "child":
        return redirect("/")

    conn = get_db_connection()

    # Get child_id
    child = conn.execute(
        "SELECT child_id FROM child WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    if not child:
        conn.close()
        return "Child not found"

    child_id = child["child_id"]

    # Fetch tasks with completion status
    tasks = conn.execute("""
    SELECT t.id, t.task_name, t.assigned_by, t.due_date,
           CASE WHEN c.completed = 1 THEN 1 ELSE 0 END AS completed
    FROM tasks t
    LEFT JOIN child_task_status c
    ON t.id = c.task_id AND c.child_id = ?
    WHERE t.child_id = ?
    ORDER BY t.due_date DESC
    LIMIT 10
""", (child_id, child_id)).fetchall()

    conn.close()

    # Calculate progress
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"] == 1)

    if total_tasks > 0:
        completion_percent = int((completed_tasks / total_tasks) * 100)
    else:
        completion_percent = 0

    return render_template(
        "child_dashboard.html",
        fullname=session["fullname"],
        tasks=tasks,
        completion_percent=completion_percent,
        completed_tasks=completed_tasks,
        total_tasks=total_tasks
    )
#complete task
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/complete_task", methods=["POST"])
def complete_task():

    task_id = request.form["task_id"]
    file = request.files["proof_image"]

    filename = None

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

    conn = get_db_connection()

    child = conn.execute(
        "SELECT child_id FROM child WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    child_id = child["child_id"]

    conn.execute("""
        INSERT INTO child_task_status (task_id, child_id, completed, proof_image)
        VALUES (?, ?, 1, ?)
    """, (task_id, child_id, filename))

    conn.commit()
    conn.close()

    return redirect("/child_dashboard")
# ---------------- ASSIGN TASK ---------------- #
@app.route("/assign_task_page")
def assign_task_page():

    conn = get_db_connection()

    parent = conn.execute(
        "SELECT parent_id FROM parent WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    parent_id = parent["parent_id"]

    # children for dropdown
    children = conn.execute(
        "SELECT child_id, name FROM child WHERE parent_id=?",
        (parent_id,)
    ).fetchall()

    # tasks assigned by this parent
    tasks = conn.execute("""
SELECT t.id, t.task_name, t.assigned_by, t.due_date,
       c.name as child_name,
       s.completed,
       s.proof_photo
FROM tasks t
JOIN child c ON t.child_id = c.child_id
LEFT JOIN child_task_status s ON t.id = s.task_id
WHERE c.parent_id = ?
ORDER BY t.id DESC
""", (parent_id,)).fetchall()

    conn.close()

    return render_template(
        "Set_Task.html",
        children=children,
        tasks=tasks
    )
@app.route("/assign_task", methods=["POST"])
def assign_task():

    child_id = request.form["child_id"]
    task_name = request.form["task_name"]
    due_date = request.form["due_date"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO tasks (child_id, task_name, assigned_by, due_date)
        VALUES (?, ?, ?, ?)
    """, (child_id, task_name, session["fullname"], due_date))

    conn.commit()
    conn.close()

    flash("Task assigned successfully ✅")

    return redirect("/assign_task_page") 

#see all tasks in child dashboard
@app.route("/see_all")
def see_all():

    conn = get_db_connection()

    tasks = conn.execute("""
    SELECT t.id, t.task_name, t.assigned_by, t.due_date,
           CASE WHEN c.completed = 1 THEN 1 ELSE 0 END AS completed
    FROM tasks t
    LEFT JOIN child_task_status c
    ON t.id = c.task_id AND c.child_id = ?
    WHERE t.child_id = ? AND (c.completed IS NULL OR c.completed = 0)
    ORDER BY t.id DESC
    LIMIT 10
    """, (child_id, child_id)).fetchall()

    conn.close()

    pending_tasks = [t for t in tasks if t["completed"] == 0]
    completed_tasks = [t for t in tasks if t["completed"] == 1]

    return render_template(
        "seeall.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )

    # veiw assigned task in child dashboard
@app.route("/view_tasks")
def view_tasks():

    conn = get_db_connection()

    tasks = conn.execute("""
    SELECT t.task_name, t.assigned_by, t.due_date,
           c.name as child_name,
           s.completed
    FROM tasks t
    JOIN child c ON t.child_id = c.child_id
    LEFT JOIN child_task_status s ON t.id = s.task_id
    """).fetchall()


    progress = conn.execute("""
    SELECT DATE(completed_time) as day,
           COUNT(*) as total
    FROM child_task_status
    WHERE completed = 1
    GROUP BY day
    """).fetchall()

    conn.close()


    days = [row["day"] for row in progress]
    counts = [row["total"] for row in progress]


    return render_template(
        "view_task.html",
        tasks=tasks,
        days=days,
        counts=counts
    )
# ------------------delete task-------------------#
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    conn = get_db_connection()

    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.execute("DELETE FROM child_task_status WHERE task_id=?", (task_id,))

    conn.commit()
    conn.close()

    flash("Task deleted successfully")

    return redirect("/assign_task_page")
# ---------------- Screen time control ---------------- #
    @app.route("/get_screen_time")
    def get_screen_time():
        conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT total_time
        FROM screen_time
        WHERE child_id = 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row:
        screen_time = row["total_time"]
    else:
        screen_time = 0

    return jsonify({"screen_time": screen_time})
#get app limit 
@app.route("/get_app_limits/<int:child_id>")
def get_app_limits(child_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT app_name, time_limit
        FROM app_restrictions
        WHERE child_id = ?
    """,(child_id,))

    rows = cursor.fetchall()

    conn.close()

    limits = []

    for row in rows:

        limits.append({
            "app_name": row["app_name"],
            "time_limit": row["time_limit"]
        })

    return jsonify(limits)
#update app limit
@app.route("/update_limit", methods=["POST"])
def update_limit():

    data = request.get_json()

    child_id = data["child_id"]
    app_name = data["app_name"]
    time_limit = data["time_limit"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE app_restrictions
        SET time_limit = ?
        WHERE child_id = ? AND app_name = ?
    """,(time_limit, child_id, app_name))

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})
#update messsages 
@app.route("/update_usage", methods=["POST"])
def update_usage():

    data = request.get_json()

    child_id = data["child_id"]
    usage = data["usage"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE screen_time
        SET total_time = ?
        WHERE child_id = ?
    """,(usage, child_id))

    conn.commit()
    conn.close()

    return jsonify({"status":"updated"})
# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)