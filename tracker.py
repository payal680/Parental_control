import time
import sqlite3
import pygetwindow as gw

DB_PATH = "database.db"

child_id = 1

while True:

    try:

        window = gw.getActiveWindow()

        if window:

            app_name = window.title

            if app_name.strip() != "":

                conn = sqlite3.connect(DB_PATH)

                conn.row_factory = sqlite3.Row

                today = time.strftime("%Y-%m-%d")

                existing = conn.execute("""
                SELECT * FROM app_usage
                WHERE child_id=? AND app_name=? AND date=?
                """, (child_id, app_name, today)).fetchone()

                if existing:

                    conn.execute("""
                    UPDATE app_usage
                    SET usage_time = usage_time + 1
                    WHERE id=?
                    """, (existing["id"],))

                else:

                    conn.execute("""
                    INSERT INTO app_usage
                    (child_id, app_name, usage_time, date)
                    VALUES (?, ?, ?, ?)
                    """, (child_id, app_name, 1, today))

                limit = conn.execute("""
                SELECT time_limit
                FROM app_restrictions
                WHERE child_id=? AND app_name=?
                """, (child_id, app_name)).fetchone()

                conn.commit()
                conn.close()

                print("Tracking:", app_name)

    except Exception as e:
        print(e)

    time.sleep(60)