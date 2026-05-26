import sqlite3
import time
import tkinter as tk
import ctypes

DB_PATH = "database.db"

child_id = 1

used_minutes = 0

def lock_screen():

    ctypes.windll.user32.LockWorkStation()

    root = tk.Tk()

    root.attributes("-fullscreen", True)

    root.configure(bg="black")

    root.bind("<Alt-F4>", lambda e: "break")

    label = tk.Label(
        root,
        text="TIME LIMIT REACHED",
        fg="white",
        bg="black",
        font=("Arial", 40, "bold")
    )

    label.pack(expand=True)

    root.mainloop()


while True:

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    limit_data = conn.execute("""
    SELECT daily_limit
    FROM screen_limits
    WHERE child_id=?
    """, (child_id,)).fetchone()

    conn.close()

    if limit_data:

        daily_limit = limit_data["daily_limit"]

        if used_minutes >= daily_limit:
            lock_screen()

    time.sleep(60)

    used_minutes += 1