import os
import sqlite3
import shutil

db_path = os.path.join(os.environ["USERPROFILE"],
                       "AppData", "Local", "Google", "Chrome",
                       "User Data", "Default", "History")

print(db_path)

temp_db = "temp_chrome_history_db"
shutil.copy2(db_path, temp_db)

try:
    connection = sqlite3.connect(temp_db)
    cursor = connection.cursor()

    cursor.execute("select url_for_display, normalized_url from clusters_and_visits")

    rows = cursor.fetchall()

    for row in rows:
        title, url = row
        print(f"{title} - {url}")

    connection.close()

except Exception as e:
    print("error {e}")

finally:
    os.remove(temp_db)